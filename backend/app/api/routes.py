"""
API Endpoints for Soil Health, Crop Recommendation,
Smart Irrigation, Weather, and Chat
"""

from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy.orm import Session
from sqlalchemy import desc


from backend.app.database.session import get_db

from backend.app.database.models import (
    SoilRecord,
    IrrigationRecommendation
)


from backend.app.schemas.common import (
    SoilAnalysisInput,
    SoilAnalysisResult,

    CropRecommendationInput,
    CropRecommendationResult,

    IrrigationCalculationInput,
    IrrigationAdviceResult,

    CurrentWeatherResponse,
    WeatherForecastResponse,

    ChatRequest,
    ChatResponse
)


from backend.app.services.soil_service import SoilService
from backend.app.services.crop_service import CropService
from backend.app.services.irrigation_service import IrrigationService
from backend.app.services.weather_service import WeatherService
from backend.app.services.chat_service import ChatService


# =========================================================
# SOIL ROUTER
# =========================================================

soil_router = APIRouter(
    prefix="/api/soil",
    tags=["Soil Health"]
)


@soil_router.post(
    "/analyze",
    response_model=SoilAnalysisResult
)
def analyze_soil_sample(
    data: SoilAnalysisInput,
    db: Session = Depends(get_db)
):

    """
    Analyze soil NPK, pH, and organic carbon
    and return diagnostic ratings.
    """

    return SoilService.analyze_soil(
        data,
        db
    )


@soil_router.get("/records")
def get_soil_records(
    limit: int = 10,
    db: Session = Depends(get_db)
):

    """
    Get recent soil analysis records.
    """

    return (
        db.query(SoilRecord)
        .order_by(
            desc(SoilRecord.created_at)
        )
        .limit(limit)
        .all()
    )


# =========================================================
# CROP RECOMMENDATION ROUTER
# =========================================================

crop_router = APIRouter(
    prefix="/api/crop",
    tags=["Crop Recommendation"]
)


@crop_router.post(
    "/recommend",
    response_model=CropRecommendationResult
)
def recommend_crops(
    data: CropRecommendationInput
):

    """
    Recommend best-suited crops based on
    soil nutrients, season, and climate.
    """

    return CropService.recommend_crops(
        data
    )


# =========================================================
# SMART IRRIGATION ROUTER
# =========================================================

irrigation_router = APIRouter(
    prefix="/api/irrigation",
    tags=["Smart Irrigation"]
)


@irrigation_router.post(
    "/calculate",
    response_model=IrrigationAdviceResult
)
def calculate_irrigation(
    data: IrrigationCalculationInput,
    db: Session = Depends(get_db)
):

    """
    Calculate rule-based precision irrigation
    requirements and scheduling.
    """

    return IrrigationService.calculate_irrigation_advice(
        data,
        db
    )


@irrigation_router.get("/history")
def get_irrigation_history(
    limit: int = 10,
    db: Session = Depends(get_db)
):

    """
    Get recent irrigation recommendations.
    """

    return (
        db.query(IrrigationRecommendation)
        .order_by(
            desc(IrrigationRecommendation.created_at)
        )
        .limit(limit)
        .all()
    )


# =========================================================
# WEATHER ROUTER
# =========================================================

weather_router = APIRouter(
    prefix="/api/weather",
    tags=["Weather"]
)


# =========================================================
# CURRENT WEATHER
# =========================================================

@weather_router.get(
    "/current",
    response_model=CurrentWeatherResponse
)
def get_current_weather(

    city: Optional[str] = Query(
        default=None,
        description=(
            "City name. Optional when "
            "latitude and longitude are provided."
        )
    ),

    lat: Optional[float] = Query(
        default=None,
        description="Current GPS latitude."
    ),

    lon: Optional[float] = Query(
        default=None,
        description="Current GPS longitude."
    )

):

    """
    Get current weather conditions
    and agricultural alerts.

    Location priority:

    1. Latitude + longitude
    2. City name

    No hard-coded Pune location.
    """


    # =====================================================
    # VALIDATE GPS PAIR
    # =====================================================

    if (
        (lat is not None and lon is None)
        or
        (lat is None and lon is not None)
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Both latitude and longitude "
                "are required."
            )
        )


    # =====================================================
    # LOCATION REQUIRED
    # =====================================================

    if (
        lat is None
        and lon is None
        and not city
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Location is required. "
                "Provide latitude/longitude "
                "or city."
            )
        )


    # =====================================================
    # CALL WEATHER SERVICE
    # =====================================================

    result = WeatherService.get_weather(

        city=city,

        lat=lat,

        lon=lon

    )


    # =====================================================
    # HANDLE WEATHER ERROR
    # =====================================================

    if "error" in result:

        raise HTTPException(
            status_code=502,
            detail=result.get(
                "message",
                "Unable to fetch weather."
            )
        )


    # =====================================================
    # RETURN CURRENT WEATHER
    # =====================================================

    return result["current"]


# =========================================================
# WEATHER FORECAST
# =========================================================

@weather_router.get(
    "/forecast",
    response_model=WeatherForecastResponse
)
def get_weather_forecast(

    city: Optional[str] = Query(
        default=None,
        description=(
            "City name. Optional when "
            "latitude and longitude are provided."
        )
    ),

    lat: Optional[float] = Query(
        default=None,
        description="Current GPS latitude."
    ),

    lon: Optional[float] = Query(
        default=None,
        description="Current GPS longitude."
    )

):

    """
    Get agricultural weather forecast.

    Location priority:

    1. Latitude + longitude
    2. City name

    No hard-coded Pune location.
    """


    # =====================================================
    # VALIDATE GPS PAIR
    # =====================================================

    if (
        (lat is not None and lon is None)
        or
        (lat is None and lon is not None)
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Both latitude and longitude "
                "are required."
            )
        )


    # =====================================================
    # LOCATION REQUIRED
    # =====================================================

    if (
        lat is None
        and lon is None
        and not city
    ):

        raise HTTPException(
            status_code=400,
            detail=(
                "Location is required. "
                "Provide latitude/longitude "
                "or city."
            )
        )


    # =====================================================
    # CALL WEATHER SERVICE
    # =====================================================

    result = WeatherService.get_weather(

        city=city,

        lat=lat,

        lon=lon

    )


    # =====================================================
    # HANDLE WEATHER ERROR
    # =====================================================

    if "error" in result:

        raise HTTPException(
            status_code=502,
            detail=result.get(
                "message",
                "Unable to fetch weather."
            )
        )


    # =====================================================
    # RETURN WEATHER + FORECAST
    # =====================================================

    return result


# =========================================================
# CHAT ROUTER
# =========================================================

chat_router = APIRouter(
    prefix="/api/chat",
    tags=["AI Assistant"]
)


@chat_router.post(
    "",
    response_model=ChatResponse
)
def chat_with_agri_assistant(
    req: ChatRequest
):

    """
    Interact with multilingual AI Agricultural Assistant
    (English + Marathi).
    """

    history_dicts = [

        {
            "role": message.role,
            "content": message.content
        }

        for message in (
            req.conversation_history or []
        )

    ]


    return ChatService.get_response(

        message=req.message,

        language=req.language,

        conversation_history=history_dicts

    )