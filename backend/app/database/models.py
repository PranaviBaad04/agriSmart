"""
SQLAlchemy Database Models for AgriSmart Platform
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, default="Smart Farmer")
    email = Column(String(120), unique=True, index=True, nullable=True)
    language = Column(String(10), default="en")  # 'en' or 'mr'
    created_at = Column(DateTime, default=datetime.utcnow)

    detections = relationship("DiseaseDetection", back_populates="user", cascade="all, delete-orphan")


class DiseaseDetection(Base):
    __tablename__ = "disease_detections"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    crop = Column(String(50), default="Chilli (Capsicum annuum)")
    image_url = Column(String(500), nullable=False)
    cloudinary_public_id = Column(String(255), nullable=True)
    disease = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)
    severity = Column(String(50), nullable=False)
    severity_level = Column(Integer, default=1)
    lesion_coverage_percent = Column(Float, default=0.0)
    recommendation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="detections")


class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    device_id = Column(String(50), default="ESP32_001", index=True)
    soil_moisture = Column(Float, nullable=False)
    ph = Column(Float, nullable=True)
    nitrogen = Column(Float, nullable=True)
    phosphorus = Column(Float, nullable=True)
    potassium = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    rain_detected = Column(Boolean, default=False)
    is_demo = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class IrrigationRecommendation(Base):
    __tablename__ = "irrigation_recommendations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    soil_moisture = Column(Float, nullable=False)
    weather_condition = Column(String(100), default="Clear")
    crop = Column(String(50), default="Chilli")
    recommendation = Column(Text, nullable=False)
    water_level = Column(String(50), default="Moderate")
    timing = Column(String(100), default="Early Morning")
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class SoilRecord(Base):
    __tablename__ = "soil_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sample_name = Column(String(100), default="Plot A - Field Soil")
    ph = Column(Float, nullable=False)
    nitrogen = Column(Float, nullable=False)
    phosphorus = Column(Float, nullable=False)
    potassium = Column(Float, nullable=False)
    organic_carbon = Column(Float, default=0.65)
    overall_status = Column(String(50), default="Optimal")
    recommendations = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
