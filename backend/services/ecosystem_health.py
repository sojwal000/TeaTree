"""
Ecosystem Health Index (EHI) Service.
Calculates a transparent weighted Ecosystem Health Index (0-100) based on
Soil quality, Temperature, Humidity, Rainfall, and Wild Tea Tree Health scores.
"""
import math
from typing import Dict, Any, Optional


def calculate_soil_component(ph: float = 5.2, soc: float = 1.4) -> float:
    """Normalize soil parameters to 0-100 scale based on tea plant preferences."""
    # Optimal pH for wild tea trees is 4.5 to 5.5
    if 4.5 <= ph <= 5.5:
        ph_score = 100.0
    elif ph < 4.5:
        ph_score = max(0.0, 100.0 - (4.5 - ph) * 40.0)
    else:
        ph_score = max(0.0, 100.0 - (ph - 5.5) * 35.0)

    # Optimal Organic Carbon is >= 1.2%
    if soc >= 1.2:
        soc_score = 100.0
    else:
        soc_score = max(0.0, (soc / 1.2) * 100.0)

    return round((ph_score * 0.6) + (soc_score * 0.4), 1)


def calculate_temperature_component(temp_c: float = 23.5) -> float:
    """Normalize temperature to 0-100 scale (optimal 20-26°C for wild tea)."""
    if 20.0 <= temp_c <= 26.0:
        return 100.0
    elif temp_c < 20.0:
        return max(0.0, round(100.0 - (20.0 - temp_c) * 8.0, 1))
    else:
        return max(0.0, round(100.0 - (temp_c - 26.0) * 12.0, 1))


def calculate_humidity_component(humidity_pct: float = 78.0) -> float:
    """Normalize relative humidity to 0-100 scale (optimal 65-85%)."""
    if 65.0 <= humidity_pct <= 85.0:
        return 100.0
    elif humidity_pct < 65.0:
        return max(0.0, round(100.0 - (65.0 - humidity_pct) * 3.0, 1))
    else:
        return max(0.0, round(100.0 - (humidity_pct - 85.0) * 4.0, 1))


def calculate_rainfall_component(monthly_rainfall_mm: float = 160.0) -> float:
    """Normalize rainfall to 0-100 scale (optimal 100-300 mm/month or ~1500-3500 mm/yr)."""
    if 100.0 <= monthly_rainfall_mm <= 300.0:
        return 100.0
    elif monthly_rainfall_mm < 100.0:
        return max(0.0, round((monthly_rainfall_mm / 100.0) * 100.0, 1))
    else:
        return max(0.0, round(100.0 - (monthly_rainfall_mm - 300.0) * 0.2, 1))


def calculate_ecosystem_health_index(
    ph: float = 5.2,
    soc: float = 1.4,
    temp_c: float = 23.5,
    humidity_pct: float = 78.0,
    rainfall_mm: float = 160.0,
    tree_health_score: float = 78.0,
    region_name: str = "Overall Region"
) -> Dict[str, Any]:
    """
    Computes Ecosystem Health Index (0-100) using transparent weights:
    - Soil component: 20%
    - Temperature component: 20%
    - Humidity component: 15%
    - Rainfall component: 15%
    - Tree health component: 30%
    """
    soil_score = calculate_soil_component(ph, soc)
    temp_score = calculate_temperature_component(temp_c)
    hum_score = calculate_humidity_component(humidity_pct)
    rain_score = calculate_rainfall_component(rainfall_mm)
    tree_score = max(0.0, min(100.0, float(tree_health_score)))

    # Weights sum to 100%
    w_soil = 0.20
    w_temp = 0.20
    w_hum = 0.15
    w_rain = 0.15
    w_tree = 0.30

    ehi_score = round(
        (soil_score * w_soil) +
        (temp_score * w_temp) +
        (hum_score * w_hum) +
        (rain_score * w_rain) +
        (tree_score * w_tree),
        1
    )

    if ehi_score >= 80.0:
        status = "Healthy"
        symbol = "🟢"
    elif ehi_score >= 50.0:
        status = "Moderate"
        symbol = "🟡"
    else:
        status = "Poor"
        symbol = "🔴"

    return {
        "region": region_name,
        "ecosystem_health_index": ehi_score,
        "status": status,
        "status_symbol": symbol,
        "components": {
            "soil": {"score": soil_score, "weight": "20%", "contribution": round(soil_score * w_soil, 1)},
            "temperature": {"score": temp_score, "weight": "20%", "contribution": round(temp_score * w_temp, 1)},
            "humidity": {"score": hum_score, "weight": "15%", "contribution": round(hum_score * w_hum, 1)},
            "rainfall": {"score": rain_score, "weight": "15%", "contribution": round(rain_score * w_rain, 1)},
            "tree_health": {"score": tree_score, "weight": "30%", "contribution": round(tree_score * w_tree, 1)},
        },
        "raw_inputs": {
            "ph": ph,
            "organic_carbon_pct": soc,
            "temperature_c": temp_c,
            "humidity_pct": humidity_pct,
            "rainfall_mm": rainfall_mm,
            "tree_health_score": tree_health_score
        },
        "formula": "EHI = 0.20*Soil + 0.20*Temp + 0.15*Humidity + 0.15*Rainfall + 0.30*TreeHealth"
    }
