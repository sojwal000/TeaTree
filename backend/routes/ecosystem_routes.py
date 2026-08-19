"""
Ecosystem Health Router.
Provides APIs for fetching Ecosystem Health Index (EHI) scores for overall region or specific sub-regions.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from backend.database import get_database
from backend.services.ecosystem_health import calculate_ecosystem_health_index
from backend.routes.soil_routes import fetch_soil_grids, get_soil_props_fallback

router = APIRouter(prefix="/api/ecosystem", tags=["Ecosystem Health"])


@router.get("/health")
async def get_ecosystem_health(
    region: Optional[str] = Query(None, description="Optional region name to filter by")
):
    """
    Get Ecosystem Health Index (0-100) based on MongoDB tree records, soil health, and environmental data.
    """
    db = get_database()
    query = {}
    if region:
        query["location_name"] = {"$regex": f"^{region}", "$options": "i"}

    cursor = db.trees.find(query)
    trees = await cursor.to_list(length=1000)

    if not trees and region:
        # Fallback query if region not found exact
        cursor = db.trees.find({})
        trees = await cursor.to_list(length=1000)

    if not trees:
        # Default baseline if database empty
        res = calculate_ecosystem_health_index(
            ph=5.2, soc=1.4, temp_c=23.0, humidity_pct=76.0, rainfall_mm=170.0, tree_health_score=75.0, region_name=region or "Overall Region"
        )
        return res

    # Compute averages across trees in region
    total_health = 0.0
    count = 0
    lat_sum = 0.0
    lon_sum = 0.0

    for t in trees:
        h = t.get("health_score")
        if h is None:
            # Check latest health score or default
            h = 76.5
        total_health += float(h)
        count += 1
        lat_sum += float(t.get("latitude", 26.75))
        lon_sum += float(t.get("longitude", 94.20))

    avg_tree_health = total_health / count if count > 0 else 75.0
    avg_lat = lat_sum / count if count > 0 else 26.75
    avg_lon = lon_sum / count if count > 0 else 94.20

    # Fetch soil parameters
    soil_props = await fetch_soil_grids(avg_lat, avg_lon)
    if not soil_props:
        soil_props = get_soil_props_fallback(avg_lat, avg_lon)

    ph_val = soil_props.get("ph") or 5.2
    soc_val = soil_props.get("soc") or 1.4

    # Fetch latest environmental data from DB if present
    env_data = await db.environmental_data.find_one({"tree_id": trees[0]["tree_id"]})
    if env_data:
        temp_val = float(env_data.get("temperature", 23.5))
        hum_val = float(env_data.get("humidity", 78.0))
        rain_val = float(env_data.get("precipitation", 160.0)) if "precipitation" in env_data else 160.0
    else:
        temp_val = 23.5
        hum_val = 78.0
        rain_val = 160.0

    res = calculate_ecosystem_health_index(
        ph=ph_val,
        soc=soc_val,
        temp_c=temp_val,
        humidity_pct=hum_val,
        rainfall_mm=rain_val,
        tree_health_score=avg_tree_health,
        region_name=region or "Overall Region"
    )

    res["tree_count"] = count
    res["average_latitude"] = round(avg_lat, 4)
    res["average_longitude"] = round(avg_lon, 4)

    return res


@router.get("/health/{region_id}")
async def get_region_ecosystem_health(region_id: str):
    """Get Ecosystem Health Index for a specific named region."""
    return await get_ecosystem_health(region=region_id)
