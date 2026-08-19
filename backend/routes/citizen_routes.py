"""
Citizen-Science Tree Data Collection Routes.
Allows community members, farmers, researchers, and trekkers to submit wild tea tree sightings
with GPS coordinates, photo, and observational metrics.
"""
import os
import uuid
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form, Query
from pydantic import BaseModel
from backend.database import get_database

router = APIRouter(prefix="/api/citizen", tags=["Citizen Science"])

UPLOAD_DIR = "uploads"
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


class StatusUpdateModel(BaseModel):
    status: str  # "pending", "validated", "rejected"


@router.post("/sightings")
async def submit_sighting(
    latitude: float = Form(...),
    longitude: float = Form(...),
    location_name: str = Form(...),
    notes: str = Form(...),
    tree_name: Optional[str] = Form(None),
    estimated_height: Optional[float] = Form(None),
    estimated_diameter: Optional[float] = Form(None),
    estimated_ring_count: Optional[int] = Form(None),
    file: UploadFile = File(...)
):
    """
    Submit a citizen-science tree sighting with GPS location, photo, and observation notes.
    Initial validation checks range, photo format, and field bounds.
    """
    # 1. Coordinate validation
    if not (-90.0 <= latitude <= 90.0):
        raise HTTPException(status_code=400, detail="Latitude must be between -90 and 90 degrees")
    if not (-180.0 <= longitude <= 180.0):
        raise HTTPException(status_code=400, detail="Longitude must be between -180 and 180 degrees")

    # 2. Prevent absurd 0.0, 0.0 coordinates unless explicitly intended
    if abs(latitude) < 0.0001 and abs(longitude) < 0.0001:
        raise HTTPException(status_code=400, detail="Invalid GPS location detected (0.0, 0.0)")

    # 3. Notes length check
    if len(notes.strip()) < 3:
        raise HTTPException(status_code=400, detail="Observation notes must be at least 3 characters long")
    if len(notes) > 1000:
        raise HTTPException(status_code=400, detail="Observation notes cannot exceed 1000 characters")

    # 4. Photo validation
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only JPG, JPEG, PNG, and WEBP images are supported")

    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Image file size must be under 10 MB")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    sighting_id = str(uuid.uuid4())
    filename = f"citizen_{sighting_id[:8]}_{uuid.uuid4().hex[:6]}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(contents)

    photo_url = f"/uploads/{filename}"

    # 5. Build submission document
    sighting_doc = {
        "sighting_id": sighting_id,
        "photo_url": photo_url,
        "latitude": latitude,
        "longitude": longitude,
        "location_name": location_name.strip(),
        "notes": notes.strip(),
        "tree_name": tree_name.strip() if tree_name else "Wild Tea Tree",
        "estimated_height": estimated_height,
        "estimated_diameter": estimated_diameter,
        "estimated_ring_count": estimated_ring_count,
        "submitted_at": datetime.utcnow(),
        "validation_status": "pending",  # "pending", "validated", "rejected"
    }

    db = get_database()
    await db.citizen_sightings.insert_one(sighting_doc)

    # Return response without _id
    sighting_doc.pop("_id", None)
    return {
        "message": "Citizen sighting submitted successfully and queued for validation.",
        "sighting": sighting_doc
    }


@router.get("/sightings")
async def get_sightings(
    status: Optional[str] = Query(None, description="Filter by status: pending, validated, rejected"),
    limit: int = Query(100, ge=1, le=500)
):
    """
    Get all citizen-submitted sightings.
    """
    db = get_database()
    query = {}
    if status and status.lower() in {"pending", "validated", "rejected"}:
        query["validation_status"] = status.lower()

    cursor = db.citizen_sightings.find(query, {"_id": 0}).sort("submitted_at", -1).limit(limit)
    sightings = await cursor.to_list(length=limit)
    return {"sightings": sightings, "count": len(sightings)}


@router.get("/sightings/{sighting_id}")
async def get_sighting_detail(sighting_id: str):
    """Get single citizen sighting detail."""
    db = get_database()
    sighting = await db.citizen_sightings.find_one({"sighting_id": sighting_id}, {"_id": 0})
    if not sighting:
        raise HTTPException(status_code=404, detail="Sighting not found")
    return sighting


@router.patch("/sightings/{sighting_id}/status")
async def update_sighting_status(sighting_id: str, body: StatusUpdateModel):
    """Update validation status of a sighting ("pending", "validated", "rejected")."""
    valid_statuses = {"pending", "validated", "rejected"}
    if body.status.lower() not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Status must be one of {valid_statuses}")

    db = get_database()
    res = await db.citizen_sightings.update_one(
        {"sighting_id": sighting_id},
        {"$set": {"validation_status": body.status.lower(), "updated_at": datetime.utcnow()}}
    )
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Sighting not found")

    return {"message": f"Sighting status updated to '{body.status.lower()}'", "sighting_id": sighting_id}
