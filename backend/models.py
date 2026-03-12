"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# ─── Auth Models ────────────────────────────────────────────────
class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    user_id: str
    name: str
    email: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None


# ─── Tree Models ────────────────────────────────────────────────
class TreeCreate(BaseModel):
    height: float = Field(..., gt=0, description="Tree height in meters")
    diameter: float = Field(..., gt=0, description="Trunk diameter in cm")
    ring_count: Optional[int] = Field(None, ge=0, description="Growth ring count")
    elevation: float = Field(..., description="Elevation in meters")
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    location_name: str = Field(..., min_length=1, max_length=200)
    images: Optional[List[str]] = []


class TreeUpdate(BaseModel):
    height: Optional[float] = Field(None, gt=0)
    diameter: Optional[float] = Field(None, gt=0)
    ring_count: Optional[int] = Field(None, ge=0)
    elevation: Optional[float] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    location_name: Optional[str] = Field(None, max_length=200)
    images: Optional[List[str]] = None


class TreeResponse(BaseModel):
    tree_id: str
    height: float
    diameter: float
    ring_count: Optional[int] = None
    elevation: float
    latitude: float
    longitude: float
    location_name: str
    images: List[str] = []
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# ─── Environmental Data Models ──────────────────────────────────
class EnvironmentalDataCreate(BaseModel):
    tree_id: str
    temperature: Optional[float] = Field(None, description="Temperature in °C")
    humidity: Optional[float] = Field(None, ge=0, le=100, description="Humidity %")
    wind_speed: Optional[float] = Field(None, ge=0, description="Wind speed in m/s")
    co2_level: Optional[float] = Field(None, ge=0, description="CO2 level in ppm")


class EnvironmentalDataResponse(BaseModel):
    record_id: str
    tree_id: str
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    wind_speed: Optional[float] = None
    co2_level: Optional[float] = None
    timestamp: datetime


# ─── Analytics Models ───────────────────────────────────────────
class CorrelationResult(BaseModel):
    variables: List[str]
    correlation_matrix: dict
    p_values: Optional[dict] = None


class RegressionResult(BaseModel):
    model_type: str
    coefficients: dict
    r_squared: float
    predictions: Optional[List[dict]] = None


class StatsSummary(BaseModel):
    total_trees: int
    avg_height: float
    avg_diameter: float
    avg_elevation: float
    elevation_range: dict
    diameter_range: dict
    location_counts: dict


# ─── Search / Filter Models ────────────────────────────────────
class TreeFilter(BaseModel):
    location_name: Optional[str] = None
    min_elevation: Optional[float] = None
    max_elevation: Optional[float] = None
    min_diameter: Optional[float] = None
    max_diameter: Optional[float] = None
    min_height: Optional[float] = None
    max_height: Optional[float] = None
