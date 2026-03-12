"""
Real-Time Climate Data routes using Open-Meteo API (FREE, no API key required).
Provides current weather, hourly/daily forecasts, and historical data for tree locations.
"""
import httpx
from typing import Optional
from fastapi import APIRouter, HTTPException, Query
from backend.database import get_database

router = APIRouter(prefix="/api/climate", tags=["Climate"])

OPEN_METEO_BASE = "https://api.open-meteo.com/v1"


@router.get("/current")
async def get_current_weather(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
):
    """Get current weather for given coordinates using Open-Meteo."""
    url = (
        f"{OPEN_METEO_BASE}/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m,"
        f"precipitation,weather_code,surface_pressure,cloud_cover"
        f"&timezone=auto"
    )
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.get(url)
            resp.raise_for_status()
        except httpx.HTTPError:
            raise HTTPException(status_code=502, detail="Failed to fetch weather data from Open-Meteo")

    data = resp.json()
    current = data.get("current", {})

    return {
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "timezone": data.get("timezone"),
        "current": {
            "temperature": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "wind_speed": current.get("wind_speed_10m"),
            "precipitation": current.get("precipitation"),
            "weather_code": current.get("weather_code"),
            "pressure": current.get("surface_pressure"),
            "cloud_cover": current.get("cloud_cover"),
            "weather_description": _weather_code_to_text(current.get("weather_code")),
        },
    }


@router.get("/forecast")
async def get_forecast(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    days: int = Query(7, ge=1, le=16),
):
    """Get daily weather forecast for up to 16 days."""
    url = (
        f"{OPEN_METEO_BASE}/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,"
        f"wind_speed_10m_max,precipitation_probability_max,weather_code"
        f"&timezone=auto&forecast_days={days}"
    )
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.get(url)
            resp.raise_for_status()
        except httpx.HTTPError:
            raise HTTPException(status_code=502, detail="Failed to fetch forecast data")

    data = resp.json()
    daily = data.get("daily", {})
    dates = daily.get("time", [])

    forecast = []
    for i, date in enumerate(dates):
        forecast.append({
            "date": date,
            "temp_max": daily.get("temperature_2m_max", [None])[i] if i < len(daily.get("temperature_2m_max", [])) else None,
            "temp_min": daily.get("temperature_2m_min", [None])[i] if i < len(daily.get("temperature_2m_min", [])) else None,
            "precipitation": daily.get("precipitation_sum", [None])[i] if i < len(daily.get("precipitation_sum", [])) else None,
            "wind_speed_max": daily.get("wind_speed_10m_max", [None])[i] if i < len(daily.get("wind_speed_10m_max", [])) else None,
            "precip_probability": daily.get("precipitation_probability_max", [None])[i] if i < len(daily.get("precipitation_probability_max", [])) else None,
            "weather_code": daily.get("weather_code", [None])[i] if i < len(daily.get("weather_code", [])) else None,
            "weather_description": _weather_code_to_text(daily.get("weather_code", [None])[i]) if i < len(daily.get("weather_code", [])) else None,
        })

    return {"latitude": data.get("latitude"), "longitude": data.get("longitude"), "forecast": forecast}


@router.get("/hourly")
async def get_hourly_forecast(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
    hours: int = Query(24, ge=1, le=168),
):
    """Get hourly weather forecast."""
    url = (
        f"{OPEN_METEO_BASE}/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,"
        f"precipitation,wind_speed_10m,soil_temperature_0cm,soil_moisture_0_to_1cm"
        f"&timezone=auto&forecast_hours={hours}"
    )
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.get(url)
            resp.raise_for_status()
        except httpx.HTTPError:
            raise HTTPException(status_code=502, detail="Failed to fetch hourly data")

    data = resp.json()
    hourly = data.get("hourly", {})
    times = hourly.get("time", [])

    records = []
    for i, t in enumerate(times):
        records.append({
            "time": t,
            "temperature": hourly.get("temperature_2m", [None])[i] if i < len(hourly.get("temperature_2m", [])) else None,
            "humidity": hourly.get("relative_humidity_2m", [None])[i] if i < len(hourly.get("relative_humidity_2m", [])) else None,
            "precipitation": hourly.get("precipitation", [None])[i] if i < len(hourly.get("precipitation", [])) else None,
            "precip_probability": hourly.get("precipitation_probability", [None])[i] if i < len(hourly.get("precipitation_probability", [])) else None,
            "wind_speed": hourly.get("wind_speed_10m", [None])[i] if i < len(hourly.get("wind_speed_10m", [])) else None,
            "soil_temperature": hourly.get("soil_temperature_0cm", [None])[i] if i < len(hourly.get("soil_temperature_0cm", [])) else None,
            "soil_moisture": hourly.get("soil_moisture_0_to_1cm", [None])[i] if i < len(hourly.get("soil_moisture_0_to_1cm", [])) else None,
        })

    return {"latitude": data.get("latitude"), "longitude": data.get("longitude"), "hourly": records}


@router.get("/tree/{tree_id}")
async def get_tree_climate(tree_id: str):
    """Get current weather at a specific tree's location."""
    db = get_database()
    tree = await db.trees.find_one({"tree_id": tree_id})
    if not tree:
        raise HTTPException(status_code=404, detail="Tree not found")

    url = (
        f"{OPEN_METEO_BASE}/forecast?"
        f"latitude={tree['latitude']}&longitude={tree['longitude']}"
        f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m,"
        f"precipitation,weather_code,surface_pressure"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code"
        f"&timezone=auto&forecast_days=7"
    )
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            resp = await client.get(url)
            resp.raise_for_status()
        except httpx.HTTPError:
            raise HTTPException(status_code=502, detail="Failed to fetch climate data for tree")

    data = resp.json()
    current = data.get("current", {})
    daily = data.get("daily", {})
    dates = daily.get("time", [])

    forecast = []
    for i, date in enumerate(dates):
        forecast.append({
            "date": date,
            "temp_max": daily.get("temperature_2m_max", [None])[i] if i < len(daily.get("temperature_2m_max", [])) else None,
            "temp_min": daily.get("temperature_2m_min", [None])[i] if i < len(daily.get("temperature_2m_min", [])) else None,
            "precipitation": daily.get("precipitation_sum", [None])[i] if i < len(daily.get("precipitation_sum", [])) else None,
            "weather_description": _weather_code_to_text(daily.get("weather_code", [None])[i]) if i < len(daily.get("weather_code", [])) else None,
        })

    return {
        "tree_id": tree_id,
        "location_name": tree.get("location_name"),
        "latitude": tree["latitude"],
        "longitude": tree["longitude"],
        "current": {
            "temperature": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "wind_speed": current.get("wind_speed_10m"),
            "precipitation": current.get("precipitation"),
            "pressure": current.get("surface_pressure"),
            "weather_description": _weather_code_to_text(current.get("weather_code")),
        },
        "forecast_7day": forecast,
    }


def _weather_code_to_text(code):
    """Convert WMO weather code to human-readable text."""
    if code is None:
        return "Unknown"
    codes = {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Foggy", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
        80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
        95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail",
    }
    return codes.get(code, f"Code {code}")
