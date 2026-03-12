"""
AI-based Tea Tree Health Prediction routes.
Uses image color analysis (Pillow + numpy) to assess tree health from uploaded photos.
Analyzes green channel intensity, brown spot ratio, leaf discoloration, and canopy density.
"""
import os
import uuid
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Query
from backend.database import get_database
from backend.auth import get_current_user

router = APIRouter(prefix="/api/health", tags=["Health Prediction"])

UPLOAD_DIR = "uploads"


def _analyze_image(img):
    """Analyze a PIL Image and return health metrics."""
    import numpy as np

    img_rgb = img.convert("RGB")
    arr = np.array(img_rgb, dtype=np.float64)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

    # Greenness index: excess green = 2*G - R - B
    total = r + g + b + 1e-6
    excess_green = (2 * g - r - b)
    green_ratio = np.mean(g / total)
    avg_excess_green = np.clip(np.mean(excess_green) / 255, -1, 1)

    # Brown/yellow detection: high R, medium G, low B
    brown_mask = (r > 100) & (g > 50) & (g < 180) & (b < 100) & (r > g)
    brown_ratio = np.mean(brown_mask.astype(float))

    # Dark spot detection (potential disease): very dark pixels
    brightness = np.mean(arr, axis=2)
    dark_ratio = np.mean((brightness < 40).astype(float))

    # Canopy density estimation: green-dominant pixels
    green_dominant = (g > r) & (g > b) & (g > 60)
    canopy_density = np.mean(green_dominant.astype(float))

    # Leaf discoloration: yellow-ish pixels
    yellow_mask = (r > 150) & (g > 150) & (b < 100)
    yellow_ratio = np.mean(yellow_mask.astype(float))

    # Health score calculation (0-100)
    score = 50.0
    score += green_ratio * 40          # More green = healthier (max +40)
    score += avg_excess_green * 20     # Excess green bonus (max +20)
    score -= brown_ratio * 60          # Brown spots penalty
    score -= dark_ratio * 30           # Dark spots penalty
    score += canopy_density * 15       # Dense canopy bonus
    score -= yellow_ratio * 40         # Yellow/chlorosis penalty
    score = max(0, min(100, score))

    # Determine status
    if score >= 80:
        health_status = "Healthy"
    elif score >= 60:
        health_status = "Moderate"
    elif score >= 40:
        health_status = "At Risk"
    else:
        health_status = "Unhealthy"

    # Identify issues
    issues = []
    if brown_ratio > 0.05:
        issues.append({"type": "Brown Spots", "severity": "High" if brown_ratio > 0.15 else "Medium",
                        "description": f"Brown/necrotic areas detected ({brown_ratio*100:.1f}% of image)"})
    if yellow_ratio > 0.03:
        issues.append({"type": "Chlorosis", "severity": "High" if yellow_ratio > 0.10 else "Medium",
                        "description": f"Yellowing leaves detected ({yellow_ratio*100:.1f}% of image)"})
    if dark_ratio > 0.08:
        issues.append({"type": "Dark Lesions", "severity": "Medium",
                        "description": f"Dark spots/lesions detected ({dark_ratio*100:.1f}% of image)"})
    if canopy_density < 0.25:
        issues.append({"type": "Sparse Canopy", "severity": "Medium" if canopy_density > 0.10 else "High",
                        "description": f"Low canopy density ({canopy_density*100:.1f}%)"})

    # Recommendations
    recommendations = []
    if health_status == "Healthy":
        recommendations.append("Continue current maintenance practices")
        recommendations.append("Monitor periodically for early signs of stress")
    else:
        if brown_ratio > 0.05:
            recommendations.append("Inspect for fungal or bacterial infection on brown areas")
            recommendations.append("Consider applying appropriate fungicide treatment")
        if yellow_ratio > 0.03:
            recommendations.append("Check soil nutrient levels, possible nitrogen or iron deficiency")
            recommendations.append("Evaluate watering schedule — chlorosis may indicate overwatering")
        if canopy_density < 0.25:
            recommendations.append("Assess environmental stressors (drought, pests, soil quality)")
            recommendations.append("Consider soil amendment and fertilization program")
        if dark_ratio > 0.08:
            recommendations.append("Examine dark spots closely for signs of disease or pest damage")

    return {
        "health_score": round(score, 1),
        "health_status": health_status,
        "metrics": {
            "green_ratio": round(float(green_ratio), 4),
            "excess_green_index": round(float(avg_excess_green), 4),
            "brown_spot_ratio": round(float(brown_ratio), 4),
            "canopy_density": round(float(canopy_density), 4),
            "yellow_ratio": round(float(yellow_ratio), 4),
            "dark_spot_ratio": round(float(dark_ratio), 4),
        },
        "issues": issues,
        "recommendations": recommendations,
    }


@router.post("/{tree_id}/check")
async def health_check(
    tree_id: str,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
):
    """Analyze an uploaded tree image to predict health status."""
    from PIL import Image
    import io as _io

    db = get_database()
    tree = await db.trees.find_one({"tree_id": tree_id})
    if not tree:
        raise HTTPException(status_code=404, detail="Tree not found")

    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
        raise HTTPException(status_code=400, detail="Only JPG, PNG, WEBP images are accepted")

    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image must be under 10 MB")

    try:
        img = Image.open(_io.BytesIO(contents))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

    analysis = _analyze_image(img)

    # Save image
    filename = f"health_{tree_id}_{uuid.uuid4().hex[:8]}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(contents)

    # Store result in DB
    record = {
        "record_id": str(uuid.uuid4()),
        "tree_id": tree_id,
        "image_path": f"/uploads/{filename}",
        "analyzed_by": current_user["user_id"],
        "analyzed_at": datetime.utcnow(),
        **analysis,
    }
    await db.health_records.insert_one(record)
    record.pop("_id", None)

    return record


@router.get("/{tree_id}/history")
async def get_health_history(
    tree_id: str,
    limit: int = Query(20, ge=1, le=100),
):
    """Get health check history for a tree."""
    db = get_database()
    cursor = db.health_records.find(
        {"tree_id": tree_id},
        {"_id": 0},
    ).sort("analyzed_at", -1).limit(limit)
    records = await cursor.to_list(length=limit)
    return records


@router.get("/summary")
async def health_summary():
    """Get platform-wide health summary statistics."""
    db = get_database()

    pipeline = [
        {"$sort": {"analyzed_at": -1}},
        {"$group": {
            "_id": "$tree_id",
            "latest_score": {"$first": "$health_score"},
            "latest_status": {"$first": "$health_status"},
            "check_count": {"$sum": 1},
        }},
        {"$group": {
            "_id": None,
            "total_checked": {"$sum": 1},
            "avg_score": {"$avg": "$latest_score"},
            "healthy": {"$sum": {"$cond": [{"$eq": ["$latest_status", "Healthy"]}, 1, 0]}},
            "moderate": {"$sum": {"$cond": [{"$eq": ["$latest_status", "Moderate"]}, 1, 0]}},
            "at_risk": {"$sum": {"$cond": [{"$eq": ["$latest_status", "At Risk"]}, 1, 0]}},
            "unhealthy": {"$sum": {"$cond": [{"$eq": ["$latest_status", "Unhealthy"]}, 1, 0]}},
            "total_checks": {"$sum": "$check_count"},
        }},
    ]
    result = await db.health_records.aggregate(pipeline).to_list(length=1)
    if not result:
        return {"total_checked": 0, "avg_score": 0, "healthy": 0, "moderate": 0,
                "at_risk": 0, "unhealthy": 0, "total_checks": 0}
    data = result[0]
    data.pop("_id", None)
    data["avg_score"] = round(data.get("avg_score", 0), 1)
    return data
