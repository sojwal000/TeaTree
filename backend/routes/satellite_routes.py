"""
Satellite Vegetation / NDVI Monitoring routes.
Uses NASA POWER API (FREE, no API key required) for vegetation-related climate parameters.
Computes a proxy vegetation health index from temperature, precipitation, and solar radiation.
"""
import httpx
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from backend.database import get_database

router = APIRouter(prefix="/api/satellite", tags=["Satellite / NDVI"])

NASA_POWER_BASE = "https://power.larc.nasa.gov/api/temporal/daily/point"


@router.get("/vegetation/{tree_id}")
async def get_vegetation_data(
    tree_id: str,
    days: int = Query(30, ge=7, le=365),
):
    """
    Get vegetation-related environmental data for a specific tree location
    using NASA POWER API. Computes a proxy Vegetation Health Index (VHI).
    """
    db = get_database()
    tree = await db.trees.find_one({"tree_id": tree_id})
    if not tree:
        raise HTTPException(status_code=404, detail="Tree not found")

    return await _fetch_vegetation_data(tree["latitude"], tree["longitude"], days, tree_id)


@router.get("/vegetation")
async def get_vegetation_by_coords(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    days: int = Query(30, ge=7, le=365),
):
    """Get vegetation data for arbitrary coordinates."""
    return await _fetch_vegetation_data(lat, lon, days)


@router.get("/region-summary")
async def get_region_vegetation_summary():
    """
    Get vegetation health summary across all tree locations.
    Groups by location and returns average vegetation index.
    """
    db = get_database()
    pipeline = [
        {"$group": {
            "_id": "$location_name",
            "avg_lat": {"$avg": "$latitude"},
            "avg_lon": {"$avg": "$longitude"},
            "tree_count": {"$sum": 1},
        }},
        {"$sort": {"tree_count": -1}},
        {"$limit": 15},
    ]
    locations = await db.trees.aggregate(pipeline).to_list(length=15)

    results = []
    end = datetime.utcnow()
    start = end - timedelta(days=30)
    start_str = start.strftime("%Y%m%d")
    end_str = end.strftime("%Y%m%d")

    async with httpx.AsyncClient(timeout=30.0) as client:
        for loc in locations:
            try:
                url = (
                    f"{NASA_POWER_BASE}?"
                    f"parameters=T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,ALLSKY_SFC_SW_DWN"
                    f"&community=AG&longitude={loc['avg_lon']}&latitude={loc['avg_lat']}"
                    f"&start={start_str}&end={end_str}&format=JSON"
                )
                resp = await client.get(url)
                if resp.status_code != 200:
                    results.append({
                        "location": loc["_id"],
                        "tree_count": loc["tree_count"],
                        "vegetation_index": None,
                        "status": "Data unavailable",
                    })
                    continue

                data = resp.json()
                params = data.get("properties", {}).get("parameter", {})
                t2m = params.get("T2M", {})
                precip = params.get("PRECTOTCORR", {})
                solar = params.get("ALLSKY_SFC_SW_DWN", {})

                # Filter out fill values (-999)
                t_vals = [v for v in t2m.values() if v > -900]
                p_vals = [v for v in precip.values() if v > -900]
                s_vals = [v for v in solar.values() if v > -900]

                avg_temp = sum(t_vals) / len(t_vals) if t_vals else 0
                total_precip = sum(p_vals)
                avg_solar = sum(s_vals) / len(s_vals) if s_vals else 0

                vhi = _compute_vegetation_health_index(avg_temp, total_precip, avg_solar)

                results.append({
                    "location": loc["_id"],
                    "tree_count": loc["tree_count"],
                    "avg_temperature": round(avg_temp, 1),
                    "total_precipitation_mm": round(total_precip, 1),
                    "avg_solar_radiation": round(avg_solar, 2),
                    "vegetation_index": round(vhi, 1),
                    "status": _vhi_status(vhi),
                })
            except Exception:
                results.append({
                    "location": loc["_id"],
                    "tree_count": loc["tree_count"],
                    "vegetation_index": None,
                    "status": "Error fetching data",
                })

    return {"locations": results, "period_days": 30}


async def _fetch_vegetation_data(lat: float, lon: float, days: int, tree_id: str = None):
    """Fetch NASA POWER data and compute vegetation health metrics."""
    end = datetime.utcnow()
    start = end - timedelta(days=days)
    start_str = start.strftime("%Y%m%d")
    end_str = end.strftime("%Y%m%d")

    url = (
        f"{NASA_POWER_BASE}?"
        f"parameters=T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,ALLSKY_SFC_SW_DWN,RH2M,WS2M"
        f"&community=AG&longitude={lon}&latitude={lat}"
        f"&start={start_str}&end={end_str}&format=JSON"
    )

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.get(url)
            resp.raise_for_status()
        except httpx.HTTPError:
            raise HTTPException(status_code=502, detail="Failed to fetch data from NASA POWER API")

    data = resp.json()
    params = data.get("properties", {}).get("parameter", {})

    t2m = params.get("T2M", {})
    t_max = params.get("T2M_MAX", {})
    t_min = params.get("T2M_MIN", {})
    precip = params.get("PRECTOTCORR", {})
    solar = params.get("ALLSKY_SFC_SW_DWN", {})
    humidity = params.get("RH2M", {})
    wind = params.get("WS2M", {})

    # Build daily records (filter out NASA fill values = -999)
    daily_records = []
    for date_key in sorted(t2m.keys()):
        rec = {"date": f"{date_key[:4]}-{date_key[4:6]}-{date_key[6:8]}"}
        t_val = t2m.get(date_key)
        rec["temperature"] = round(t_val, 1) if t_val and t_val > -900 else None
        rec["temp_max"] = round(t_max.get(date_key, -999), 1) if t_max.get(date_key, -999) > -900 else None
        rec["temp_min"] = round(t_min.get(date_key, -999), 1) if t_min.get(date_key, -999) > -900 else None
        rec["precipitation"] = round(precip.get(date_key, -999), 2) if precip.get(date_key, -999) > -900 else None
        rec["solar_radiation"] = round(solar.get(date_key, -999), 2) if solar.get(date_key, -999) > -900 else None
        rec["humidity"] = round(humidity.get(date_key, -999), 1) if humidity.get(date_key, -999) > -900 else None
        rec["wind_speed"] = round(wind.get(date_key, -999), 1) if wind.get(date_key, -999) > -900 else None
        daily_records.append(rec)

    # Compute summary stats
    t_vals = [r["temperature"] for r in daily_records if r["temperature"] is not None]
    p_vals = [r["precipitation"] for r in daily_records if r["precipitation"] is not None]
    s_vals = [r["solar_radiation"] for r in daily_records if r["solar_radiation"] is not None]
    h_vals = [r["humidity"] for r in daily_records if r["humidity"] is not None]

    avg_temp = sum(t_vals) / len(t_vals) if t_vals else 0
    total_precip = sum(p_vals)
    avg_solar = sum(s_vals) / len(s_vals) if s_vals else 0
    avg_humidity = sum(h_vals) / len(h_vals) if h_vals else 0

    vhi = _compute_vegetation_health_index(avg_temp, total_precip, avg_solar)

    result = {
        "latitude": lat,
        "longitude": lon,
        "period": {"start": start.strftime("%Y-%m-%d"), "end": end.strftime("%Y-%m-%d"), "days": days},
        "summary": {
            "avg_temperature": round(avg_temp, 1),
            "total_precipitation_mm": round(total_precip, 1),
            "avg_solar_radiation": round(avg_solar, 2),
            "avg_humidity": round(avg_humidity, 1),
            "vegetation_health_index": round(vhi, 1),
            "vegetation_status": _vhi_status(vhi),
        },
        "daily": daily_records,
    }
    if tree_id:
        result["tree_id"] = tree_id

    return result


def _compute_vegetation_health_index(avg_temp: float, total_precip: float, avg_solar: float) -> float:
    """
    Compute a proxy Vegetation Health Index (0-100) based on climate parameters.
    Optimal conditions for tea trees: 15-25°C, moderate rainfall, good solar radiation.
    """
    # Temperature component (optimal 15-25°C for tea trees)
    if 15 <= avg_temp <= 25:
        temp_score = 100
    elif 10 <= avg_temp < 15 or 25 < avg_temp <= 30:
        temp_score = 70
    elif 5 <= avg_temp < 10 or 30 < avg_temp <= 35:
        temp_score = 40
    else:
        temp_score = 15

    # Precipitation component (monthly, optimal 100-300mm for tea)
    monthly_precip = total_precip * (30.0 / max(1, total_precip))  # normalize
    monthly_precip = total_precip  # direct value for monthly
    if 80 <= monthly_precip <= 350:
        precip_score = 100
    elif 40 <= monthly_precip < 80 or 350 < monthly_precip <= 500:
        precip_score = 65
    elif 20 <= monthly_precip < 40 or 500 < monthly_precip <= 700:
        precip_score = 35
    else:
        precip_score = 15

    # Solar radiation component (optimal 10-25 MJ/m²/day for tea)
    if 10 <= avg_solar <= 25:
        solar_score = 100
    elif 5 <= avg_solar < 10 or 25 < avg_solar <= 30:
        solar_score = 70
    else:
        solar_score = 40

    # Weighted average
    vhi = temp_score * 0.40 + precip_score * 0.35 + solar_score * 0.25
    return max(0, min(100, vhi))


def _vhi_status(vhi: float) -> str:
    if vhi >= 80:
        return "Excellent"
    elif vhi >= 60:
        return "Good"
    elif vhi >= 40:
        return "Moderate"
    elif vhi >= 20:
        return "Poor"
    else:
        return "Critical"
