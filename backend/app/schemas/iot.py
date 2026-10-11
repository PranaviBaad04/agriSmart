"""
Pydantic Schemas for IoT Telemetry & ESP32 Integration
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class SensorDataInput(BaseModel):
    device_id: str = Field(default="ESP32_001", description="Unique ESP32 device identifier")
    soil_moisture: float = Field(..., ge=0.0, le=100.0, description="Volumetric Soil Moisture in %")
    # Optional: a sensor may be missing or fail to read (sent as null / omitted)
    ph: Optional[float] = Field(default=None, ge=0.0, le=14.0, description="Soil pH value")
    nitrogen: Optional[float] = Field(default=None, ge=0.0, description="Nitrogen content in mg/kg")
    phosphorus: Optional[float] = Field(default=None, ge=0.0, description="Phosphorus content in mg/kg")
    potassium: Optional[float] = Field(default=None, ge=0.0, description="Potassium content in mg/kg")
    temperature: Optional[float] = Field(default=None, description="Ambient temperature in °C")
    humidity: Optional[float] = Field(default=None, ge=0.0, le=100.0, description="Relative humidity in %")
    rain_detected: bool = Field(default=False, description="Rain sensor digital/analog trigger")
    is_demo: Optional[bool] = Field(default=False, description="Flag indicating simulated demo reading")
    pump_on: Optional[bool] = Field(default=None, description="Actual pump relay state reported by the device")


class SensorDataResponse(BaseModel):
    id: int
    device_id: str
    soil_moisture: float
    ph: Optional[float] = None
    nitrogen: Optional[float] = None
    phosphorus: Optional[float] = None
    potassium: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    rain_detected: bool
    is_demo: bool
    timestamp: datetime

    class Config:
        from_attributes = True


class IoTStatusSummary(BaseModel):
    mode: str  # "demo" or "live"
    device_id: str
    latest: Optional[SensorDataResponse] = None
    moisture_status: str
    ph_status: str
    npk_status: str
    temp_humidity_status: str
    rain_status: str
    battery_level: Optional[int] = 94
    signal_strength_dbm: Optional[int] = -62
    last_updated: datetime


class PumpStatus(BaseModel):
    desired: str
    actual: Optional[str] = None
    device_online: bool
    last_report_age_seconds: Optional[float] = None
    on_remaining_seconds: Optional[int] = None
    max_run_minutes: int


class PumpCommand(BaseModel):
    command: str
