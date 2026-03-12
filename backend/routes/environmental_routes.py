"""
Environmental data routes
"""
import uuid
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query
from backend.database import get_database
from backend.models import EnvironmentalDataCreate, EnvironmentalDataResponse
from backend.auth import get_current_user

router = APIRouter(prefix="/api/environmental", tags=["Environmental Data"])


@router.post("", response_model=EnvironmentalDataResponse, status_code=status.HTTP_201_CREATED)
async def create_environmental_record(
    data: EnvironmentalDataCreate,
    current_user: dict = Depends(get_current_user),
):
    """Record environmental data linked to a tree."""
    db = get_database()

    # Verify tree exists
    tree = await db.trees.find_one({"tree_id": data.tree_id})
    if not tree:
        raise HTTPException(status_code=404, detail="Tree not found")

    record = {
        "record_id": str(uuid.uuid4()),
        **data.model_dump(),
        "timestamp": datetime.utcnow(),
    }
    await db.environmental_data.insert_one(record)
    return EnvironmentalDataResponse(**record)


@router.get("", response_model=list[EnvironmentalDataResponse])
async def get_environmental_data(
    tree_id: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """Retrieve environmental data records, optionally filtered by tree_id."""
    db = get_database()
    query = {}
    if tree_id:
        query["tree_id"] = tree_id

    cursor = db.environmental_data.find(query).skip(skip).limit(limit).sort("timestamp", -1)
    records = await cursor.to_list(length=limit)
    return [EnvironmentalDataResponse(**r) for r in records]


@router.get("/summary")
async def get_environmental_summary(tree_id: Optional[str] = None):
    """Get summary statistics of environmental data."""
    db = get_database()
    match_stage = {}
    if tree_id:
        match_stage = {"tree_id": tree_id}

    pipeline = [
        {"$match": match_stage} if match_stage else {"$match": {}},
        {
            "$group": {
                "_id": None,
                "avg_temperature": {"$avg": "$temperature"},
                "min_temperature": {"$min": "$temperature"},
                "max_temperature": {"$max": "$temperature"},
                "avg_humidity": {"$avg": "$humidity"},
                "min_humidity": {"$min": "$humidity"},
                "max_humidity": {"$max": "$humidity"},
                "avg_wind_speed": {"$avg": "$wind_speed"},
                "avg_co2": {"$avg": "$co2_level"},
                "max_co2": {"$max": "$co2_level"},
                "record_count": {"$sum": 1},
            }
        },
    ]

    result = await db.environmental_data.aggregate(pipeline).to_list(length=1)
    if not result:
        return {"message": "No environmental data found"}

    summary = result[0]
    summary.pop("_id", None)
    # Round values
    for key, val in summary.items():
        if isinstance(val, float):
            summary[key] = round(val, 2)
    return summary


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_environmental_record(record_id: str, current_user: dict = Depends(get_current_user)):
    """Delete an environmental data record."""
    db = get_database()
    result = await db.environmental_data.delete_one({"record_id": record_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Record not found")
