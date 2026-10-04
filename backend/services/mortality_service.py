"""
Tea Tree Mortality Risk Assessment Service

This is a rule-based research/prototype risk model.
It does NOT claim to biologically predict the exact death
of a tea tree.

It uses information already available in the TeaTree platform:
- AI health score
- health history
- temperature
- humidity
- rainfall / precipitation
- soil moisture when available
- Ecosystem Health Index when available
- estimated age / ring count
"""

from typing import Optional, List, Dict, Any


def clamp(value: float, minimum: float = 0, maximum: float = 100) -> float:
    return max(minimum, min(maximum, value))


def temperature_stress(temp: Optional[float]) -> float:
    """
    Returns environmental stress from 0-100.

    The ranges here are prototype thresholds for the project,
    not a validated mortality model.
    """

    if temp is None:
        return 20

    if 18 <= temp <= 28:
        return 0

    if 14 <= temp < 18 or 28 < temp <= 32:
        return 30

    if 10 <= temp < 14 or 32 < temp <= 36:
        return 60

    return 90


def humidity_stress(humidity: Optional[float]) -> float:

    if humidity is None:
        return 20

    if 60 <= humidity <= 90:
        return 0

    if 45 <= humidity < 60 or 90 < humidity <= 95:
        return 35

    return 75


def rainfall_stress(rainfall: Optional[float]) -> float:

    if rainfall is None:
        return 20

    if 100 <= rainfall <= 300:
        return 0

    if 60 <= rainfall < 100 or 300 < rainfall <= 400:
        return 30

    if 25 <= rainfall < 60 or 400 < rainfall <= 500:
        return 60

    return 85


def soil_moisture_stress(value: Optional[float]) -> float:

    if value is None:
        return 20

    if 45 <= value <= 80:
        return 0

    if 30 <= value < 45 or 80 < value <= 90:
        return 35

    return 80


def age_stress(ring_count: Optional[int]) -> float:

    if ring_count is None:
        return 10

    if ring_count < 80:
        return 5

    if ring_count < 130:
        return 15

    if ring_count < 180:
        return 30

    return 50


def calculate_health_trend(
    health_history: List[Dict[str, Any]]
) -> Dict[str, Any]:

    if not health_history:
        return {
            "trend": "unknown",
            "change": 0,
            "stress": 15
        }

    scores = []

    for record in health_history:

        score = record.get("health_score")

        if score is None:
            score = record.get("score")

        if isinstance(score, (int, float)):
            scores.append(float(score))

    if len(scores) < 2:
        return {
            "trend": "insufficient_history",
            "change": 0,
            "stress": 10
        }

    oldest = scores[-1]
    newest = scores[0]

    change = newest - oldest

    if change <= -30:
        return {
            "trend": "rapid_decline",
            "change": round(change, 2),
            "stress": 100
        }

    if change <= -15:
        return {
            "trend": "declining",
            "change": round(change, 2),
            "stress": 70
        }

    if change <= -5:
        return {
            "trend": "slight_decline",
            "change": round(change, 2),
            "stress": 40
        }

    if change >= 10:
        return {
            "trend": "improving",
            "change": round(change, 2),
            "stress": 0
        }

    return {
        "trend": "stable",
        "change": round(change, 2),
        "stress": 10
    }


def calculate_mortality_risk(
    tree: Dict[str, Any],
    latest_environment: Optional[Dict[str, Any]] = None,
    health_history: Optional[List[Dict[str, Any]]] = None,
    ecosystem_health_index: Optional[float] = None,
) -> Dict[str, Any]:

    latest_environment = latest_environment or {}
    health_history = health_history or []

    # ---------------------------------------------------------
    # CURRENT HEALTH
    # ---------------------------------------------------------

    health_score = tree.get("health_score")

    if health_score is None and health_history:

        health_score = health_history[0].get(
            "health_score",
            health_history[0].get("score")
        )

    if health_score is None:
        health_score = 70

    health_score = clamp(float(health_score))

    health_risk = 100 - health_score

    # ---------------------------------------------------------
    # ENVIRONMENT
    # ---------------------------------------------------------

    temperature = latest_environment.get("temperature")
    humidity = latest_environment.get("humidity")

    rainfall = latest_environment.get("rainfall")

    if rainfall is None:
        rainfall = latest_environment.get("precipitation")

    soil_moisture = latest_environment.get("soil_moisture")

    temp_risk = temperature_stress(temperature)
    humidity_risk = humidity_stress(humidity)
    rain_risk = rainfall_stress(rainfall)
    moisture_risk = soil_moisture_stress(soil_moisture)

    environmental_risk = (
        temp_risk * 0.35
        + humidity_risk * 0.20
        + rain_risk * 0.25
        + moisture_risk * 0.20
    )

    # ---------------------------------------------------------
    # HEALTH TREND
    # ---------------------------------------------------------

    trend = calculate_health_trend(health_history)

    trend_risk = trend["stress"]

    # ---------------------------------------------------------
    # ECOSYSTEM HEALTH
    # ---------------------------------------------------------

    if ecosystem_health_index is None:
        ecosystem_risk = 20
    else:
        ecosystem_risk = 100 - clamp(
            float(ecosystem_health_index)
        )

    # ---------------------------------------------------------
    # AGE
    # ---------------------------------------------------------

    age_risk = age_stress(
        tree.get("ring_count")
    )

    # ---------------------------------------------------------
    # FINAL WEIGHTED RISK
    # ---------------------------------------------------------

    risk_score = (
        health_risk * 0.40
        + environmental_risk * 0.25
        + trend_risk * 0.15
        + ecosystem_risk * 0.10
        + age_risk * 0.10
    )

    risk_score = round(
        clamp(risk_score),
        1
    )

    # ---------------------------------------------------------
    # CLASSIFICATION
    # ---------------------------------------------------------

    if risk_score < 25:

        risk_level = "Low"
        status = "Stable"
        color = "green"

    elif risk_score < 50:

        risk_level = "Moderate"
        status = "Monitor"
        color = "yellow"

    elif risk_score < 75:

        risk_level = "High"
        status = "At Risk"
        color = "orange"

    else:

        risk_level = "Critical"
        status = "Critical Intervention"
        color = "red"

    # ---------------------------------------------------------
    # REASONS
    # ---------------------------------------------------------

    factors = []

    if health_score < 40:
        factors.append(
            "Very low current health score"
        )

    elif health_score < 60:
        factors.append(
            "Reduced current health score"
        )

    if trend["trend"] in [
        "rapid_decline",
        "declining"
    ]:
        factors.append(
            "Health score is declining over time"
        )

    if temp_risk >= 60:
        factors.append(
            "Temperature stress detected"
        )

    if humidity_risk >= 60:
        factors.append(
            "Humidity outside preferred range"
        )

    if rain_risk >= 60:
        factors.append(
            "Rainfall stress detected"
        )

    if moisture_risk >= 60:
        factors.append(
            "Soil moisture stress detected"
        )

    if (
        ecosystem_health_index is not None
        and ecosystem_health_index < 50
    ):
        factors.append(
            "Poor ecosystem health conditions"
        )

    if age_risk >= 50:
        factors.append(
            "High estimated age contributes to risk"
        )

    if not factors:
        factors.append(
            "No major mortality indicators detected"
        )

    # ---------------------------------------------------------
    # RECOMMENDATIONS
    # ---------------------------------------------------------

    recommendations = []

    if risk_level == "Low":

        recommendations = [
            "Continue routine monitoring.",
            "Maintain environmental observations.",
            "Repeat health assessment periodically."
        ]

    elif risk_level == "Moderate":

        recommendations = [
            "Increase monitoring frequency.",
            "Inspect leaves, canopy, trunk and root-zone conditions.",
            "Review recent temperature, rainfall and soil moisture changes."
        ]

    elif risk_level == "High":

        recommendations = [
            "Perform a detailed field inspection.",
            "Investigate disease, water stress and environmental causes.",
            "Record new photographs and health measurements.",
            "Monitor the tree frequently for further decline."
        ]

    else:

        recommendations = [
            "Prioritize immediate field inspection.",
            "Check for severe disease, physical damage and root-zone stress.",
            "Record the tree as a critical conservation case.",
            "Prepare end-of-life documentation if mortality is confirmed."
        ]

    return {
        "tree_id": tree.get("tree_id"),

        "mortality_risk_score": risk_score,
        "risk_level": risk_level,
        "status": status,
        "color": color,

        "current_health_score": health_score,

        "health_trend": trend,

        "environment": {
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall,
            "soil_moisture": soil_moisture,
        },

        "risk_components": {
            "health": round(health_risk, 1),
            "environment": round(environmental_risk, 1),
            "health_trend": round(trend_risk, 1),
            "ecosystem": round(ecosystem_risk, 1),
            "age": round(age_risk, 1),
        },

        "ecosystem_health_index":
            ecosystem_health_index,

        "factors": factors,

        "recommendations": recommendations,

        "model_type":
            "Rule-based mortality risk assessment",

        "disclaimer":
            "Research prototype risk score. "
            "It does not predict an exact biological death date."
    }