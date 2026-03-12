"""
Tree data management routes: CRUD, CSV import, image upload, search & filter
"""
import uuid
import csv
import io
import os
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Query
from backend.database import get_database
from backend.models import TreeCreate, TreeUpdate, TreeResponse
from backend.auth import get_current_user

router = APIRouter(prefix="/api/trees", tags=["Trees"])


@router.post("", response_model=TreeResponse, status_code=status.HTTP_201_CREATED)
async def create_tree(tree: TreeCreate, current_user: dict = Depends(get_current_user)):
    """Create a new tea tree record."""
    db = get_database()
    now = datetime.utcnow()
    tree_doc = {
        "tree_id": str(uuid.uuid4()),
        **tree.model_dump(),
        "created_by": current_user["user_id"],
        "created_at": now,
        "updated_at": now,
    }
    await db.trees.insert_one(tree_doc)
    return TreeResponse(**tree_doc)


@router.get("", response_model=list[TreeResponse])
async def get_trees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    location_name: Optional[str] = None,
    min_elevation: Optional[float] = None,
    max_elevation: Optional[float] = None,
    min_diameter: Optional[float] = None,
    max_diameter: Optional[float] = None,
    min_height: Optional[float] = None,
    max_height: Optional[float] = None,
    search: Optional[str] = None,
):
    """Retrieve tea tree records with optional filtering."""
    db = get_database()
    query = {}

    if location_name:
        query["location_name"] = {"$regex": location_name, "$options": "i"}
    if search:
        query["$or"] = [
            {"location_name": {"$regex": search, "$options": "i"}},
            {"tree_id": {"$regex": search, "$options": "i"}},
        ]
    if min_elevation is not None or max_elevation is not None:
        query["elevation"] = {}
        if min_elevation is not None:
            query["elevation"]["$gte"] = min_elevation
        if max_elevation is not None:
            query["elevation"]["$lte"] = max_elevation
        if not query["elevation"]:
            del query["elevation"]
    if min_diameter is not None or max_diameter is not None:
        query["diameter"] = {}
        if min_diameter is not None:
            query["diameter"]["$gte"] = min_diameter
        if max_diameter is not None:
            query["diameter"]["$lte"] = max_diameter
        if not query["diameter"]:
            del query["diameter"]
    if min_height is not None or max_height is not None:
        query["height"] = {}
        if min_height is not None:
            query["height"]["$gte"] = min_height
        if max_height is not None:
            query["height"]["$lte"] = max_height
        if not query["height"]:
            del query["height"]

    cursor = db.trees.find(query).skip(skip).limit(limit).sort("created_at", -1)
    trees = await cursor.to_list(length=limit)
    return [TreeResponse(**t) for t in trees]


@router.get("/count")
async def get_tree_count():
    """Get total number of tree records."""
    db = get_database()
    count = await db.trees.count_documents({})
    return {"count": count}


@router.get("/{tree_id}", response_model=TreeResponse)
async def get_tree(tree_id: str):
    """Retrieve a specific tea tree record."""
    db = get_database()
    tree = await db.trees.find_one({"tree_id": tree_id})
    if not tree:
        raise HTTPException(status_code=404, detail="Tree not found")
    return TreeResponse(**tree)


@router.put("/{tree_id}", response_model=TreeResponse)
async def update_tree(tree_id: str, tree_update: TreeUpdate, current_user: dict = Depends(get_current_user)):
    """Update a tree record."""
    db = get_database()
    existing = await db.trees.find_one({"tree_id": tree_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Tree not found")

    update_data = {k: v for k, v in tree_update.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()

    await db.trees.update_one({"tree_id": tree_id}, {"$set": update_data})
    updated = await db.trees.find_one({"tree_id": tree_id})
    return TreeResponse(**updated)


@router.delete("/{tree_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tree(tree_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a tree record."""
    db = get_database()
    result = await db.trees.delete_one({"tree_id": tree_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tree not found")
    # Also delete associated environmental data
    await db.environmental_data.delete_many({"tree_id": tree_id})


ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")


@router.post("/{tree_id}/images")
async def upload_tree_images(
    tree_id: str,
    files: List[UploadFile] = File(...),
    current_user: dict = Depends(get_current_user),
):
    """Upload one or more images for a tree."""
    db = get_database()
    tree = await db.trees.find_one({"tree_id": tree_id})
    if not tree:
        raise HTTPException(status_code=404, detail="Tree not found")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    saved_paths = []

    for file in files:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in ALLOWED_IMAGE_EXTENSIONS:
            continue
        filename = f"{tree_id}_{uuid.uuid4().hex[:8]}{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        content = await file.read()
        with open(filepath, "wb") as f:
            f.write(content)
        saved_paths.append(f"/uploads/{filename}")

    if not saved_paths:
        raise HTTPException(status_code=400, detail="No valid image files provided")

    await db.trees.update_one(
        {"tree_id": tree_id},
        {"$push": {"images": {"$each": saved_paths}}}
    )

    updated = await db.trees.find_one({"tree_id": tree_id})
    return {"uploaded": len(saved_paths), "images": updated.get("images", [])}


@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    """Bulk import tree data from CSV file.
    Expected columns: height, diameter, ring_count, elevation, latitude, longitude, location_name
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    content = await file.read()
    decoded = content.decode("utf-8")
    reader = csv.DictReader(io.StringIO(decoded))

    trees_to_insert = []
    errors = []
    now = datetime.utcnow()

    for i, row in enumerate(reader, start=2):  # row 1 is header
        try:
            tree_doc = {
                "tree_id": str(uuid.uuid4()),
                "height": float(row.get("height", 0)),
                "diameter": float(row.get("diameter", 0)),
                "ring_count": int(row["ring_count"]) if row.get("ring_count") else None,
                "elevation": float(row.get("elevation", 0)),
                "latitude": float(row.get("latitude", 0)),
                "longitude": float(row.get("longitude", 0)),
                "location_name": row.get("location_name", "Unknown"),
                "images": [],
                "created_by": current_user["user_id"],
                "created_at": now,
                "updated_at": now,
            }
            trees_to_insert.append(tree_doc)
        except (ValueError, KeyError) as e:
            errors.append({"row": i, "error": str(e)})

    db = get_database()
    inserted_count = 0
    if trees_to_insert:
        result = await db.trees.insert_many(trees_to_insert)
        inserted_count = len(result.inserted_ids)

    return {
        "inserted": inserted_count,
        "errors": errors,
        "total_rows": inserted_count + len(errors),
    }
