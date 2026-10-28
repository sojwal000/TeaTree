"""Public Tree Digital Passport API.\n
Returns the tree record and public, tree-linked observations used by the passport.
Do not include account identifiers or internal moderation/user data in this response.
"""
from datetime import datetime
from typing import Any
from fastapi import APIRouter, HTTPException
from backend.database import get_database
from backend.services.mortality_service import calculate_mortality_risk
from backend.services.ecosystem_health import calculate_ecosystem_health_index
from backend.routes.soil_routes import fetch_soil_grids, get_soil_props_fallback

router = APIRouter(prefix="/api/passport", tags=["Public Tree Passport"])

PRIVATE_KEYS = {
    "_id", "created_by", "updated_by", "user_id", "analyzed_by",
    "email", "password", "hashed_password", "access_token", "token",
}


def public_document(document: dict[str, Any] | None) -> dict[str, Any] | None:
    """Convert a MongoDB document to a JSON-safe public document."""
    if not document:
        return None
    return {key: value for key, value in document.items() if key not in PRIVATE_KEYS and not key.startswith("internal_")}



async def records_for_tree(collection, tree_id: str, sort_field: str, limit: int = 100):
    cursor = collection.find({"tree_id": tree_id}, {"_id": 0}).sort(sort_field, -1).limit(limit)
    return await cursor.to_list(length=limit)



@router.get("/{tree_id}")
async def get_public_tree_passport(tree_id: str):
    """Get public passport data for one tree; intentionally does not require login."""
    db = get_database()
    tree = await db.trees.find_one({"tree_id": tree_id}, {"_id": 0})
    if not tree:
        raise HTTPException(status_code=404, detail="Tree not found")

    # Tree data and public observational history
    environmental = await records_for_tree(db.environmental_data, tree_id, "timestamp", 500)
    health_records = await records_for_tree(db.health_records, tree_id, "analyzed_at", 100)
    health_checks = await records_for_tree(db.health_checks, tree_id, "created_at", 100)
    health_history = await records_for_tree(db.health_history, tree_id, "created_at", 100)
    ecosystem_records = await records_for_tree(db.ecosystem_health, tree_id, "created_at", 100)
    death_record = await db.tree_death_records.find_one({"tree_id": tree_id}, {"_id": 0}, sort=[("recorded_at", -1)])
    anomalies = await records_for_tree(db.conservation_anomalies, tree_id, "created_at", 100)

    # Select the most recent available health assessment. TreeResponse in older
    # versions omitted health_score, so derive it from health history if needed.
    current_health = tree.get("health_score")
    current_health_status = tree.get("health_status")
    if current_health is None and health_records:
        latest = health_records[0]
        current_health = latest.get("health_score", latest.get("score"))
        current_health_status = latest.get("health_status", latest.get("status"))
    if current_health is None and health_checks:
        latest = health_checks[0]
        current_health = latest.get("health_score", latest.get("score"))
        current_health_status = latest.get("health_status", latest.get("status"))

    latest_environment = environmental[0] if environmental else None
    latest_ehi_record = ecosystem_records[0] if ecosystem_records else None
    ehi_value = None
    if latest_ehi_record:
        ehi_value = latest_ehi_record.get("ecosystem_health_index", latest_ehi_record.get("ehi"))

    # Compute a tree-location EHI when no saved per-tree EHI exists. SoilGrids
    # can fail or be unavailable; the project's deterministic fallback is used
    # and is explicitly labelled below.
    ehi_calculation = None
    soil_source = "unavailable"
    try:
        lat = float(tree.get("latitude", 0.0))
        lon = float(tree.get("longitude", 0.0))
        soil_props = await fetch_soil_grids(lat, lon)
        if soil_props:
            soil_source = "SoilGrids API"
        else:
            soil_props = get_soil_props_fallback(lat, lon)
            soil_source = "TeaTree spatial fallback model"
        latest_env = latest_environment or {}
        health_for_ehi = current_health if current_health is not None else 70.0
        ehi_calculation = calculate_ecosystem_health_index(
            ph=float(soil_props.get("ph") or 5.2),
            soc=float(soil_props.get("soc") or 1.4),
            temp_c=float(latest_env.get("temperature") or 23.5),
            humidity_pct=float(latest_env.get("humidity") or 78.0),
            rainfall_mm=float(latest_env.get("rainfall") or latest_env.get("precipitation") or 160.0),
            tree_health_score=float(health_for_ehi),
            region_name=str(tree.get("location_name") or "Tree location"),
        )
        ehi_calculation["source"] = soil_source
    except Exception:
        ehi_calculation = {"error": "EHI calculation unavailable", "source": soil_source}

    effective_ehi = ehi_value
    if effective_ehi is None and ehi_calculation:
        effective_ehi = ehi_calculation.get("ecosystem_health_index")

    # Mortality risk is the existing rule-based prototype. Keep its own
    # disclaimer and expose only when a risk record can be computed.
    mortality = calculate_mortality_risk(
        tree={**tree, "health_score": current_health},
        latest_environment=latest_environment,
        health_history=health_records or health_checks or health_history,
        ecosystem_health_index=effective_ehi,
    )

    # Do not serialize MongoDB ObjectIds or expose private author identifiers.
    tree = public_document(tree)
    tree["health_score"] = current_health
    tree["health_status"] = current_health_status

    return {
        "tree": tree,
        "health": {
            "current_score": current_health,
            "current_status": current_health_status,
            "records": [public_document(item) for item in health_records],
            "checks": [public_document(item) for item in health_checks],
            "history": [public_document(item) for item in health_history],
        },
        "environment": {
            "latest": public_document(latest_environment),
            "records": [public_document(item) for item in environmental],
        },
        "ecosystem": {
            "latest": public_document(latest_ehi_record),
            "calculated": ehi_calculation,
            "records": [public_document(item) for item in ecosystem_records],
        },
        "mortality": mortality,
        "death_record": public_document(death_record),
        "conservation_anomalies": [public_document(item) for item in anomalies],
        "metadata": {
            "generated_at": datetime.utcnow(),
            "public_profile": True,
            "data_note": "Only data linked to this tree is included. External live services may be unavailable.",
        },
    }
