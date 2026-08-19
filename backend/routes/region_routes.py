"""
Cross-Region Federated Comparison Router.
Aggregates and compares tree health, rainfall, temperature, soil suitability,
and Ecosystem Health Index across multiple geographical regions.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from backend.database import get_database
from backend.services.ecosystem_health import calculate_ecosystem_health_index
from backend.routes.soil_routes import fetch_soil_grids, get_soil_props_fallback, compile_soil_health_card

router = APIRouter(prefix="/api/regions", tags=["Region Comparison"])


async def _compute_region_metrics(region_name: str, db):
    """Compute aggregate metrics for trees in a specific region."""
    # Match location_name starting with or containing region_name
    query = {"location_name": {"$regex": f"{region_name}", "$options": "i"}}
    cursor = db.trees.find(query)
    trees = await cursor.to_list(length=1000)

    if not trees:
        return {
            "region": region_name,
            "status": "insufficient_data",
            "has_data": False,
            "message": "Insufficient data available in MongoDB for this region",
            "total_trees": 0,
            "healthy_trees": 0,
            "avg_tree_health": None,
            "avg_temperature": None,
            "avg_rainfall": None,
            "soil_suitability_score": None,
            "ecosystem_health_index": None
        }

    total_count = len(trees)
    healthy_count = 0
    total_health = 0.0
    lat_sum = 0.0
    lon_sum = 0.0

    for t in trees:
        h = t.get("health_score", 76.0)
        total_health += h
        if h >= 70.0:
            healthy_count += 1
        lat_sum += float(t.get("latitude", 26.75))
        lon_sum += float(t.get("longitude", 94.20))

    avg_health = round(total_health / total_count, 1)
    avg_lat = lat_sum / total_count
    avg_lon = lon_sum / total_count

    # Fetch soil suitability card for centroid
    soil_props = await fetch_soil_grids(avg_lat, avg_lon)
    if not soil_props:
        soil_props = get_soil_props_fallback(avg_lat, avg_lon)

    soil_card = compile_soil_health_card(avg_lat, avg_lon, soil_props)
    soil_score = soil_card["prediction"]["score"]

    # Fetch environmental data across all trees in region
    tree_ids = [t["tree_id"] for t in trees]
    env_cursor = db.environmental_data.find({"tree_id": {"$in": tree_ids}})
    env_records = await env_cursor.to_list(length=1000)

    if env_records:
        temps = [float(r["temperature"]) for r in env_records if "temperature" in r and r["temperature"] is not None]
        hums = [float(r["humidity"]) for r in env_records if "humidity" in r and r["humidity"] is not None]
        rains = [float(r.get("rainfall") or r.get("precipitation") or 180.0) for r in env_records]
        avg_temp = sum(temps) / len(temps) if temps else 23.5
        avg_hum = sum(hums) / len(hums) if hums else 78.0
        avg_rain = sum(rains) / len(rains) if rains else 180.0
    else:
        avg_temp = 23.5
        avg_hum = 78.0
        avg_rain = 180.0

    # Compute EHI
    ehi_res = calculate_ecosystem_health_index(
        ph=soil_props.get("ph", 5.2),
        soc=soil_props.get("soc", 1.4),
        temp_c=avg_temp,
        humidity_pct=avg_hum,
        rainfall_mm=avg_rain,
        tree_health_score=avg_health,
        region_name=region_name
    )

    return {
        "region": region_name,
        "status": "data_available",
        "has_data": True,
        "total_trees": total_count,
        "healthy_trees": healthy_count,
        "avg_tree_health": avg_health,
        "avg_temperature": round(avg_temp, 1),
        "avg_rainfall": round(avg_rain, 1),
        "soil_suitability_score": round(soil_score, 1),
        "ecosystem_health_index": ehi_res["ecosystem_health_index"],
        "ehi_status": ehi_res["status"],
        "ehi_details": ehi_res["components"],
        "centroid": {"latitude": round(avg_lat, 4), "longitude": round(avg_lon, 4)}
    }


@router.get("")
async def list_regions():
    """List distinct regions present in MongoDB tree database."""
    db = get_database()
    pipeline = [
        {"$group": {"_id": "$location_name", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    results = await db.trees.aggregate(pipeline).to_list(length=100)

    regions = []
    seen = set()
    for r in results:
        loc = r["_id"]
        if loc:
            primary_name = loc.split(",")[0].strip()
            if primary_name not in seen:
                seen.add(primary_name)
                regions.append({"region_id": primary_name, "location_name": loc, "tree_count": r["count"]})

    # Default sample regions if database has few
    sample_defaults = ["Jorhat", "Darjeeling", "Nilgiri Hills", "Assam", "Munnar", "Rasayani"]
    for sd in sample_defaults:
        if sd not in seen:
            # Check count
            count = await db.trees.count_documents({"location_name": {"$regex": sd, "$options": "i"}})
            regions.append({"region_id": sd, "location_name": sd, "tree_count": count})

    return {"regions": regions}


@router.get("/compare")
async def compare_regions(
    regions: str = Query(..., description="Comma-separated list of region names (e.g. Jorhat,Darjeeling,Nilgiri Hills)")
):
    """
    Compare multiple regions side by side for tree health, rainfall, temperature, soil suitability, and EHI.
    """
    db = get_database()
    region_list = [r.strip() for r in regions.split(",") if r.strip()]

    if not region_list:
        raise HTTPException(status_code=400, detail="Please provide at least one region name to compare")

    comparisons = []
    for reg in region_list:
        metrics = await _compute_region_metrics(reg, db)
        comparisons.append(metrics)

    return {
        "compared_count": len(comparisons),
        "regions": comparisons
    }


@router.get("/{region_id}/summary")
async def get_region_summary(region_id: str):
    """Get aggregated summary metrics for a single region."""
    db = get_database()
    res = await _compute_region_metrics(region_id, db)
    return res
