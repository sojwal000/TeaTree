"""
Alert & Notification System routes.
Manages alerts for weather anomalies, health warnings, and environmental thresholds.
Stores alerts in MongoDB and provides retrieval/management endpoints.
"""
import uuid
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from backend.database import get_database
from backend.auth import get_current_user

router = APIRouter(prefix="/api/alerts", tags=["Alerts"])


@router.get("")
async def get_alerts(
    status: Optional[str] = Query(None, description="Filter: active, resolved, all"),
    severity: Optional[str] = Query(None, description="Filter: critical, warning, info"),
    limit: int = Query(50, ge=1, le=200),
    skip: int = Query(0, ge=0),
):
    """Get alerts with filtering."""
    db = get_database()
    query = {}
    if status and status != "all":
        query["status"] = status
    if severity:
        query["severity"] = severity

    cursor = db.alerts.find(query, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit)
    alerts = await cursor.to_list(length=limit)
    total = await db.alerts.count_documents(query)

    return {"alerts": alerts, "total": total, "skip": skip, "limit": limit}


@router.get("/summary")
async def get_alert_summary():
    """Get alert count summary by severity and status."""
    db = get_database()
    pipeline = [
        {"$group": {
            "_id": {"severity": "$severity", "status": "$status"},
            "count": {"$sum": 1},
        }},
    ]
    results = await db.alerts.aggregate(pipeline).to_list(length=100)

    summary = {
        "total": 0,
        "active": 0,
        "resolved": 0,
        "critical": 0,
        "warning": 0,
        "info": 0,
        "by_type": {},
    }
    for r in results:
        count = r["count"]
        summary["total"] += count
        sev = r["_id"].get("severity", "info")
        st = r["_id"].get("status", "active")
        summary[sev] = summary.get(sev, 0) + count
        summary[st] = summary.get(st, 0) + count

    # Count by alert type
    type_pipeline = [
        {"$match": {"status": "active"}},
        {"$group": {"_id": "$alert_type", "count": {"$sum": 1}}},
    ]
    type_results = await db.alerts.aggregate(type_pipeline).to_list(length=50)
    for r in type_results:
        summary["by_type"][r["_id"]] = r["count"]

    return summary


@router.post("/resolve/{alert_id}")
async def resolve_alert(
    alert_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Mark an alert as resolved."""
    db = get_database()
    result = await db.alerts.update_one(
        {"alert_id": alert_id},
        {"$set": {"status": "resolved", "resolved_at": datetime.utcnow(), "resolved_by": current_user["user_id"]}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"message": "Alert resolved", "alert_id": alert_id}


@router.delete("/{alert_id}")
async def delete_alert(
    alert_id: str,
    current_user: dict = Depends(get_current_user),
):
    """Delete an alert."""
    db = get_database()
    result = await db.alerts.delete_one({"alert_id": alert_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"message": "Alert deleted"}


@router.post("/check-weather")
async def check_weather_alerts(
    current_user: dict = Depends(get_current_user),
):
    """
    Check current weather conditions at all tree locations and create alerts
    for extreme weather. Uses Open-Meteo data.
    """
    import httpx

    db = get_database()

    # Get unique locations
    pipeline = [
        {"$group": {
            "_id": "$location_name",
            "avg_lat": {"$avg": "$latitude"},
            "avg_lon": {"$avg": "$longitude"},
            "tree_count": {"$sum": 1},
        }},
    ]
    locations = await db.trees.aggregate(pipeline).to_list(length=50)

    new_alerts = []
    async with httpx.AsyncClient(timeout=15.0) as client:
        for loc in locations:
            try:
                url = (
                    f"https://api.open-meteo.com/v1/forecast?"
                    f"latitude={loc['avg_lat']}&longitude={loc['avg_lon']}"
                    f"&current=temperature_2m,wind_speed_10m,precipitation,weather_code"
                    f"&timezone=auto"
                )
                resp = await client.get(url)
                if resp.status_code != 200:
                    continue
                data = resp.json()
                current = data.get("current", {})

                temp = current.get("temperature_2m")
                wind = current.get("wind_speed_10m")
                precip = current.get("precipitation")
                weather_code = current.get("weather_code", 0)

                # Temperature alerts
                if temp is not None:
                    if temp > 38:
                        new_alerts.append(_create_alert(
                            "Extreme Heat", "critical", "weather",
                            f"Temperature at {loc['_id']} is {temp}°C — dangerous heat stress for tea trees",
                            loc["_id"], loc["tree_count"],
                        ))
                    elif temp < 0:
                        new_alerts.append(_create_alert(
                            "Frost Warning", "critical", "weather",
                            f"Temperature at {loc['_id']} is {temp}°C — frost risk for tea trees",
                            loc["_id"], loc["tree_count"],
                        ))
                    elif temp > 35:
                        new_alerts.append(_create_alert(
                            "High Temperature", "warning", "weather",
                            f"Temperature at {loc['_id']} is {temp}°C — potential heat stress",
                            loc["_id"], loc["tree_count"],
                        ))

                # Wind alerts
                if wind is not None and wind > 50:
                    new_alerts.append(_create_alert(
                        "Strong Wind", "warning", "weather",
                        f"Wind speed at {loc['_id']} is {wind} km/h — risk of branch damage",
                        loc["_id"], loc["tree_count"],
                    ))

                # Heavy rain alerts
                if precip is not None and precip > 20:
                    new_alerts.append(_create_alert(
                        "Heavy Rainfall", "warning", "weather",
                        f"Precipitation at {loc['_id']} is {precip} mm/h — flooding risk",
                        loc["_id"], loc["tree_count"],
                    ))

                # Severe weather
                if weather_code and weather_code >= 95:
                    new_alerts.append(_create_alert(
                        "Severe Weather", "critical", "weather",
                        f"Thunderstorm detected at {loc['_id']} — take precautions",
                        loc["_id"], loc["tree_count"],
                    ))

            except Exception:
                continue

    # Check health alerts — trees with low health scores
    health_pipeline = [
        {"$sort": {"analyzed_at": -1}},
        {"$group": {
            "_id": "$tree_id",
            "latest_score": {"$first": "$health_score"},
            "latest_status": {"$first": "$health_status"},
            "analyzed_at": {"$first": "$analyzed_at"},
        }},
        {"$match": {"latest_score": {"$lt": 40}}},
    ]
    unhealthy = await db.health_records.aggregate(health_pipeline).to_list(length=100)
    for h in unhealthy:
        # Check if a similar active alert already exists
        existing = await db.alerts.find_one({
            "alert_type": "health",
            "status": "active",
            "metadata.tree_id": h["_id"],
        })
        if not existing:
            tree = await db.trees.find_one({"tree_id": h["_id"]})
            loc_name = tree.get("location_name", "Unknown") if tree else "Unknown"
            new_alerts.append({
                "alert_id": str(uuid.uuid4()),
                "title": f"Low Health Score — Tree {h['_id'][:8]}",
                "severity": "critical" if h["latest_score"] < 25 else "warning",
                "alert_type": "health",
                "description": f"Tree at {loc_name} has health score {h['latest_score']:.0f}/100 ({h['latest_status']})",
                "status": "active",
                "location": loc_name,
                "trees_affected": 1,
                "metadata": {"tree_id": h["_id"], "health_score": h["latest_score"]},
                "created_at": datetime.utcnow(),
            })

    # Insert new alerts (avoid duplicates by checking recent active alerts of same type+location)
    inserted = 0
    for alert in new_alerts:
        existing = await db.alerts.find_one({
            "title": alert["title"],
            "location": alert.get("location"),
            "status": "active",
        })
        if not existing:
            await db.alerts.insert_one(alert)
            inserted += 1

    return {"checked_locations": len(locations), "new_alerts": inserted, "total_alerts_generated": len(new_alerts)}


def _create_alert(title, severity, alert_type, description, location, trees_affected):
    return {
        "alert_id": str(uuid.uuid4()),
        "title": title,
        "severity": severity,
        "alert_type": alert_type,
        "description": description,
        "status": "active",
        "location": location,
        "trees_affected": trees_affected,
        "metadata": {},
        "created_at": datetime.utcnow(),
    }
