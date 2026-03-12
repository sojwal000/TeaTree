"""
Smart Search & Report Generation routes.
Provides advanced search with fuzzy matching, and generates comprehensive research reports.
"""
import uuid
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, Depends
from backend.database import get_database
from backend.auth import get_current_user

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/search")
async def smart_search(
    q: str = Query(..., min_length=1, description="Search query"),
    category: Optional[str] = Query(None, description="Filter: location, tree_id, elevation, all"),
    limit: int = Query(50, ge=1, le=200),
):
    """
    Smart search across trees with fuzzy matching on location names, tree IDs,
    and numeric range detection for elevation/diameter/height.
    """
    db = get_database()
    query_parts = []

    # Text search on location and tree_id
    text_regex = {"$regex": q, "$options": "i"}
    if category == "location":
        query_parts.append({"location_name": text_regex})
    elif category == "tree_id":
        query_parts.append({"tree_id": text_regex})
    elif category == "elevation":
        # Try parsing as number range e.g. "1000-2000"
        rng = _parse_range(q)
        if rng:
            query_parts.append({"elevation": {"$gte": rng[0], "$lte": rng[1]}})
        else:
            try:
                val = float(q)
                query_parts.append({"elevation": {"$gte": val - 100, "$lte": val + 100}})
            except ValueError:
                query_parts.append({"location_name": text_regex})
    else:
        # Search all fields
        query_parts.append({"location_name": text_regex})
        query_parts.append({"tree_id": text_regex})
        # Try numeric match
        rng = _parse_range(q)
        if rng:
            query_parts.append({"elevation": {"$gte": rng[0], "$lte": rng[1]}})
            query_parts.append({"diameter": {"$gte": rng[0], "$lte": rng[1]}})
        else:
            try:
                val = float(q)
                query_parts.append({"elevation": {"$gte": val - 100, "$lte": val + 100}})
            except ValueError:
                pass

    if not query_parts:
        query_parts.append({"location_name": text_regex})

    mongo_query = {"$or": query_parts} if len(query_parts) > 1 else query_parts[0]

    cursor = db.trees.find(mongo_query, {"_id": 0}).limit(limit)
    results = await cursor.to_list(length=limit)

    return {
        "query": q,
        "category": category or "all",
        "count": len(results),
        "results": results,
    }


@router.get("/generate")
async def generate_report(
    scope: str = Query("full", description="Report scope: full, location, summary"),
    location: Optional[str] = None,
    current_user: dict = Depends(get_current_user),
):
    """
    Generate a comprehensive research report in JSON format.
    Scopes: full (all data), location (specific location), summary (overview only).
    """
    db = get_database()
    query = {}
    if location:
        query["location_name"] = {"$regex": location, "$options": "i"}

    # Gather tree statistics
    trees = await db.trees.find(query, {"_id": 0}).to_list(length=10000)
    if not trees:
        raise HTTPException(status_code=404, detail="No trees found for the given criteria")

    total = len(trees)
    heights = [t["height"] for t in trees if t.get("height")]
    diameters = [t["diameter"] for t in trees if t.get("diameter")]
    elevations = [t["elevation"] for t in trees if t.get("elevation")]
    ring_counts = [t["ring_count"] for t in trees if t.get("ring_count")]

    locations = {}
    for t in trees:
        loc = t.get("location_name", "Unknown")
        if loc not in locations:
            locations[loc] = {"count": 0, "heights": [], "diameters": [], "elevations": []}
        locations[loc]["count"] += 1
        locations[loc]["heights"].append(t.get("height", 0))
        locations[loc]["diameters"].append(t.get("diameter", 0))
        locations[loc]["elevations"].append(t.get("elevation", 0))

    location_summaries = {}
    for loc, data in locations.items():
        location_summaries[loc] = {
            "tree_count": data["count"],
            "avg_height": round(sum(data["heights"]) / len(data["heights"]), 2) if data["heights"] else 0,
            "avg_diameter": round(sum(data["diameters"]) / len(data["diameters"]), 2) if data["diameters"] else 0,
            "avg_elevation": round(sum(data["elevations"]) / len(data["elevations"]), 1) if data["elevations"] else 0,
            "elevation_range": [round(min(data["elevations"]), 1), round(max(data["elevations"]), 1)] if data["elevations"] else [0, 0],
        }

    # Environmental data summary
    env_query = {}
    if location:
        tree_ids = [t["tree_id"] for t in trees]
        env_query["tree_id"] = {"$in": tree_ids}

    env_pipeline = [
        {"$match": env_query} if env_query else {"$match": {}},
        {"$group": {
            "_id": None,
            "avg_temp": {"$avg": "$temperature"},
            "avg_humidity": {"$avg": "$humidity"},
            "avg_wind": {"$avg": "$wind_speed"},
            "avg_co2": {"$avg": "$co2_level"},
            "count": {"$sum": 1},
        }},
    ]
    env_result = await db.environmental_data.aggregate(env_pipeline).to_list(length=1)
    env_summary = {}
    if env_result:
        e = env_result[0]
        env_summary = {
            "total_records": e.get("count", 0),
            "avg_temperature": round(e["avg_temp"], 1) if e.get("avg_temp") else None,
            "avg_humidity": round(e["avg_humidity"], 1) if e.get("avg_humidity") else None,
            "avg_wind_speed": round(e["avg_wind"], 1) if e.get("avg_wind") else None,
            "avg_co2_level": round(e["avg_co2"], 1) if e.get("avg_co2") else None,
        }

    # Health data
    health_pipeline = [
        {"$sort": {"analyzed_at": -1}},
        {"$group": {
            "_id": "$tree_id",
            "latest_score": {"$first": "$health_score"},
            "latest_status": {"$first": "$health_status"},
        }},
        {"$group": {
            "_id": None,
            "avg_health_score": {"$avg": "$latest_score"},
            "total_checked": {"$sum": 1},
            "healthy_count": {"$sum": {"$cond": [{"$eq": ["$latest_status", "Healthy"]}, 1, 0]}},
            "at_risk_count": {"$sum": {"$cond": [{"$gte": ["$latest_status", "At Risk"]}, 1, 0]}},
        }},
    ]
    health_result = await db.health_records.aggregate(health_pipeline).to_list(length=1)
    health_summary = {}
    if health_result:
        h = health_result[0]
        health_summary = {
            "trees_checked": h.get("total_checked", 0),
            "avg_health_score": round(h.get("avg_health_score", 0), 1),
            "healthy_trees": h.get("healthy_count", 0),
        }

    report = {
        "report_id": str(uuid.uuid4()),
        "generated_at": datetime.utcnow().isoformat(),
        "generated_by": current_user["name"],
        "scope": scope,
        "filter_location": location,
        "overview": {
            "total_trees": total,
            "total_locations": len(locations),
            "avg_height_m": round(sum(heights) / len(heights), 2) if heights else 0,
            "avg_diameter_cm": round(sum(diameters) / len(diameters), 2) if diameters else 0,
            "avg_elevation_m": round(sum(elevations) / len(elevations), 1) if elevations else 0,
            "elevation_range": {
                "min": round(min(elevations), 1) if elevations else 0,
                "max": round(max(elevations), 1) if elevations else 0,
            },
            "avg_ring_count": round(sum(ring_counts) / len(ring_counts), 1) if ring_counts else 0,
        },
        "location_breakdown": location_summaries,
        "environmental_summary": env_summary,
        "health_summary": health_summary,
    }

    if scope == "full":
        report["tree_data"] = trees[:500]  # cap at 500 for full reports

    # Save report record
    await db.reports.insert_one({
        "report_id": report["report_id"],
        "generated_at": datetime.utcnow(),
        "generated_by": current_user["user_id"],
        "scope": scope,
        "location": location,
        "tree_count": total,
    })

    return report


@router.get("/history")
async def get_report_history(
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
):
    """Get previously generated reports list."""
    db = get_database()
    cursor = db.reports.find(
        {},
        {"_id": 0},
    ).sort("generated_at", -1).limit(limit)
    return await cursor.to_list(length=limit)


def _parse_range(text: str):
    """Try to parse 'min-max' range from text."""
    parts = text.replace(" ", "").split("-")
    if len(parts) == 2:
        try:
            return (float(parts[0]), float(parts[1]))
        except ValueError:
            return None
    return None
