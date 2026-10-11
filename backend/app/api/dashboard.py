"""
Dashboard Analytics and Aggregated Status Endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.database.session import get_db
from backend.app.database.models import DiseaseDetection, SensorData, SoilRecord, IrrigationRecommendation
from backend.app.services.iot_service import IoTService
from backend.app.services.weather_service import WeatherService

dashboard_router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])
auth_router = APIRouter(prefix="/api/auth", tags=["Auth"])


@dashboard_router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    """Unified endpoint returning high-level status for all dashboard widgets"""
    # 1. IoT Telemetry
    iot_status = IoTService.get_latest_telemetry(db)

    # 2. Weather
    weather = WeatherService.get_weather()["current"]

    # 3. Disease Detections Stats
    total_scans = db.query(DiseaseDetection).count()
    recent_detections = db.query(DiseaseDetection).order_by(desc(DiseaseDetection.created_at)).limit(4).all()

    # 4. Latest Irrigation
    latest_irrigation = db.query(IrrigationRecommendation).order_by(desc(IrrigationRecommendation.created_at)).first()

    # 5. Quick Health Metrics
    latest = iot_status["latest"]
    sm = latest.soil_moisture if latest and latest.soil_moisture is not None else 44.0
    ph = latest.ph if latest and latest.ph is not None else 6.4

    return {
        "telemetry": iot_status,
        "weather": weather,
        "total_scans": total_scans,
        "recent_detections": recent_detections,
        "latest_irrigation": latest_irrigation,
        "quick_status": {
            "soil_moisture": sm,
            "soil_moisture_status": "Optimal" if 35 <= sm <= 65 else ("Low" if sm < 35 else "High"),
            "ph": ph,
            "ph_status": "Ideal (6.0 - 7.0)" if 6.0 <= ph <= 7.2 else "Attention Needed",
            "field_temperature": weather["temperature_c"],
            "field_humidity": weather["humidity_percent"],
            "rain_status": iot_status["rain_status"],
            "overall_crop_health": "Good" if total_scans == 0 or (recent_detections and recent_detections[0].disease == "Healthy_Leaf") else "Requires Attention"
        }
    }


@auth_router.get("/profile")
def get_user_profile():
    return {
        "id": 1,
        "name": "Smart Farmer",
        "email": "farmer@agrismart.org",
        "farm_location": "Baramati / Pune, Maharashtra",
        "primary_crop": "Chilli (Capsicum annuum)",
        "farm_size": "3.5 Acres",
        "iot_node": "ESP32_001",
        "language_preference": "en"
    }
