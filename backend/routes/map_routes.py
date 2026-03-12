"""
Map / geospatial data routes
"""
from typing import Optional
from fastapi import APIRouter, Query
from backend.database import get_database

router = APIRouter(prefix="/api/map", tags=["Map"])


@router.get("/trees")
async def get_map_trees(
    min_elevation: Optional[float] = None,
    max_elevation: Optional[float] = None,
    location_name: Optional[str] = None,
):
    """Get tree coordinates and basic info for map visualization."""
    db = get_database()
    query = {}

    if location_name:
        query["location_name"] = {"$regex": location_name, "$options": "i"}
    if min_elevation is not None or max_elevation is not None:
        query["elevation"] = {}
        if min_elevation is not None:
            query["elevation"]["$gte"] = min_elevation
        if max_elevation is not None:
            query["elevation"]["$lte"] = max_elevation
        if not query["elevation"]:
            del query["elevation"]

    cursor = db.trees.find(
        query,
        {
            "_id": 0,
            "tree_id": 1,
            "latitude": 1,
            "longitude": 1,
            "elevation": 1,
            "height": 1,
            "diameter": 1,
            "location_name": 1,
            "ring_count": 1,
            "images": 1,
        },
    )
    trees = await cursor.to_list(length=10000)
    return {"trees": trees, "count": len(trees)}


@router.get("/clusters")
async def get_map_clusters(
    grid_size: float = Query(0.5, description="Grid size in degrees for clustering"),
):
    """Get clustered tree data for map display (large datasets)."""
    db = get_database()

    pipeline = [
        {
            "$group": {
                "_id": {
                    "lat_grid": {
                        "$multiply": [{"$floor": {"$divide": ["$latitude", grid_size]}}, grid_size]
                    },
                    "lon_grid": {
                        "$multiply": [{"$floor": {"$divide": ["$longitude", grid_size]}}, grid_size]
                    },
                },
                "count": {"$sum": 1},
                "avg_lat": {"$avg": "$latitude"},
                "avg_lon": {"$avg": "$longitude"},
                "avg_elevation": {"$avg": "$elevation"},
                "avg_diameter": {"$avg": "$diameter"},
                "locations": {"$addToSet": "$location_name"},
            }
        },
        {"$sort": {"count": -1}},
    ]

    clusters = await db.trees.aggregate(pipeline).to_list(length=1000)

    result = []
    for c in clusters:
        result.append({
            "latitude": round(c["avg_lat"], 6),
            "longitude": round(c["avg_lon"], 6),
            "count": c["count"],
            "avg_elevation": round(c["avg_elevation"], 2),
            "avg_diameter": round(c["avg_diameter"], 2),
            "locations": c["locations"],
        })

    return {"clusters": result, "total_clusters": len(result)}


@router.get("/heatmap")
async def get_heatmap_data(
    variable: str = Query("elevation", description="Variable for heatmap intensity"),
):
    """Get data for heatmap overlay on map."""
    db = get_database()
    projection = {"_id": 0, "latitude": 1, "longitude": 1}
    if variable in ["elevation", "diameter", "height"]:
        projection[variable] = 1

    cursor = db.trees.find({}, projection)
    trees = await cursor.to_list(length=10000)

    points = []
    for t in trees:
        intensity = t.get(variable, 1)
        points.append([t["latitude"], t["longitude"], intensity if intensity else 1])

    return {"points": points, "variable": variable, "count": len(points)}
