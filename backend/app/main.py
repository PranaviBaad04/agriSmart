"""
AgriSmart FastAPI Application Main Entrypoint
"""
import os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.database.session import init_db
from backend.app.api.disease import router as disease_router
from backend.app.api.iot import router as iot_router
from backend.app.api.dashboard import dashboard_router, auth_router
from backend.app.api.routes import soil_router, crop_router, irrigation_router, weather_router, chat_router
from backend.app.services.disease_service import DiseaseService

# Create uploads directory if not present
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
UPLOADS_DIR = ROOT_DIR / "backend" / "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize DB and load ML model in memory
    print("Initializing AgriSmart database...")
    init_db()
    print("Preloading Chilli Disease ML Predictor...")
    try:
        DiseaseService.get_predictor()
    except Exception as e:
        print(f"Notice during model warmup: {e}")
    yield
    # Shutdown
    print("AgriSmart backend shutting down cleanly.")


app = FastAPI(
    title="AgriSmart: IoT & AI Smart Agriculture API",
    description="Full-stack AI- and IoT-powered Smart Agriculture System featuring Deep Learning Chilli Disease Detection, Cloudinary Storage, ESP32 Telemetry, Smart Irrigation, and Multilingual Agronomy Chatbot.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for Frontend Development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local demo/production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve uploaded images statically (fallback for local storage)
app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")

# Include Routers
app.include_router(dashboard_router)
app.include_router(auth_router)
app.include_router(disease_router)
app.include_router(iot_router)
app.include_router(soil_router)
app.include_router(crop_router)
app.include_router(irrigation_router)
app.include_router(weather_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "project": "AgriSmart: Smart Agriculture Platform",
        "status": "online",
        "version": "1.0.0",
        "docs_url": "/docs",
        "endpoints": {
            "disease_predict": "/api/disease/predict",
            "disease_history": "/api/disease/history",
            "iot_telemetry": "/api/iot/latest",
            "dashboard_summary": "/api/dashboard/summary",
            "smart_irrigation": "/api/irrigation/calculate",
            "soil_analysis": "/api/soil/analyze",
            "crop_recommendation": "/api/crop/recommend",
            "weather_forecast": "/api/weather/forecast",
            "ai_chat": "/api/chat"
        }
    }
