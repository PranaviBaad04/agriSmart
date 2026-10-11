"""
Pydantic Schemas for Soil, Crop, Irrigation, Weather, and AI Chat
"""
from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field


# --- Soil Health Schemas ---
class SoilAnalysisInput(BaseModel):
    sample_name: Optional[str] = "Main Chilli Plot"
    ph: float = Field(..., ge=3.0, le=10.0, description="Soil pH")
    nitrogen: float = Field(..., ge=0.0, le=500.0, description="Available N in kg/ha or mg/kg")
    phosphorus: float = Field(..., ge=0.0, le=300.0, description="Available P in kg/ha or mg/kg")
    potassium: float = Field(..., ge=0.0, le=500.0, description="Available K in kg/ha or mg/kg")
    organic_carbon: Optional[float] = Field(default=0.65, ge=0.0, le=5.0, description="Organic Carbon %")
    soil_type: Optional[str] = "Sandy Loam / Loamy"


class NutrientRating(BaseModel):
    value: float
    unit: str
    status: str  # "Deficient", "Low", "Optimal", "High"
    optimal_range: str
    advice_en: str
    advice_mr: str


class SoilAnalysisResult(BaseModel):
    sample_name: str
    ph_rating: NutrientRating
    nitrogen_rating: NutrientRating
    phosphorus_rating: NutrientRating
    potassium_rating: NutrientRating
    organic_carbon_rating: NutrientRating
    overall_health_score: int  # 0 to 100
    overall_status: str
    fertilizer_recommendations_en: List[str]
    fertilizer_recommendations_mr: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)


# --- Crop Recommendation Schemas ---
class CropRecommendationInput(BaseModel):
    season: str = Field(default="Kharif", description="Kharif, Rabi, Zaid / Summer")
    region: str = Field(default="Maharashtra / Western India", description="Agricultural agro-climatic zone")
    soil_type: str = Field(default="Black Cotton / Loamy", description="Soil texture")
    ph: float = Field(default=6.5, ge=3.0, le=10.0)
    nitrogen: float = Field(default=120.0, ge=0.0)
    phosphorus: float = Field(default=45.0, ge=0.0)
    potassium: float = Field(default=60.0, ge=0.0)
    temperature: Optional[float] = Field(default=28.0)
    humidity: Optional[float] = Field(default=65.0)
    rainfall_annual_mm: Optional[float] = Field(default=850.0)


class RecommendedCropItem(BaseModel):
    crop_name: str
    marathi_name: str
    suitability_score: int  # 0 - 100%
    category: str
    duration_days: str
    expected_yield_per_acre: str
    water_requirement: str
    soil_ph_ideal: str
    reasons_en: List[str]
    reasons_mr: List[str]


class CropRecommendationResult(BaseModel):
    recommended_crops: List[RecommendedCropItem]
    primary_recommendation: str
    soil_suitability_summary: str
    input_parameters: Dict[str, Any]


# --- Smart Irrigation Schemas ---
class IrrigationCalculationInput(BaseModel):
    crop: str = Field(default="Chilli (Capsicum annuum)")
    crop_growth_stage: str = Field(default="Flowering & Fruit Development")
    soil_moisture: float = Field(..., ge=0.0, le=100.0)
    soil_type: Optional[str] = "Loamy"
    temperature: Optional[float] = 30.0
    humidity: Optional[float] = 60.0
    rain_detected: Optional[bool] = False
    rain_probability_next_24h: Optional[int] = 10


class IrrigationAdviceResult(BaseModel):
    irrigation_required: bool
    urgency_level: str  # "Immediate", "Scheduled", "Not Needed", "Excess Moisture Warning"
    water_requirement_liters_per_acre: int
    recommended_duration_minutes: int
    recommended_timing: str
    reason_en: str
    reason_mr: str
    action_items_en: List[str]
    action_items_mr: List[str]
    method: str = "Rule-based Agronomic Water Balance Model"
    created_at: datetime = Field(default_factory=datetime.utcnow)


# --- Weather Schemas ---
class CurrentWeatherResponse(BaseModel):
    location: str
    temperature_c: float
    feels_like_c: float
    humidity_percent: int
    rainfall_mm: float
    wind_speed_kmh: float
    weather_condition: str
    weather_icon: str
    uv_index: float
    pressure_hpa: int
    rain_probability_percent: int
    forecast_summary_en: str
    forecast_summary_mr: str
    agricultural_alert: Optional[str] = None


class WeatherForecastDay(BaseModel):
    date: str
    day_name: str
    temp_max_c: float
    temp_min_c: float
    humidity_percent: int
    rain_probability: int
    condition: str
    icon: str


class WeatherForecastResponse(BaseModel):
    current: CurrentWeatherResponse
    forecast: List[WeatherForecastDay]


# --- AI Chat Schemas ---
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    language: str = Field(default="en", description="'en' for English, 'mr' for Marathi")
    conversation_history: Optional[List[ChatMessage]] = []
    context_data: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    reply: str
    language: str
    suggested_questions: List[str]
    source: str  # "llm" or "expert_agronomy_system"
