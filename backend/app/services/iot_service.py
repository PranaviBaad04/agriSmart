"""
IoT Telemetry Service: Supports ESP32 Ingestion & Dynamic Demo Simulation Mode
"""
import random
import math
from datetime import datetime, timedelta
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import desc

from backend.app.database.models import SensorData
from backend.app.schemas.iot import SensorDataInput, IoTStatusSummary, SensorDataResponse


class IoTService:
    _demo_mode: bool = True  # Defaults to Demo Mode until real ESP32 connected

    @classmethod
    def set_demo_mode(cls, enabled: bool):
        cls._demo_mode = enabled
        return cls._demo_mode

    @classmethod
    def is_demo_mode(cls) -> bool:
        return cls._demo_mode

    @classmethod
    def generate_simulated_reading(cls, device_id: str = "ESP32_DEMO_01") -> Dict[str, Any]:
        """
        Generate realistic simulated telemetry:
        - Soil Moisture: 38% - 55%
        - pH: 6.2 - 6.8 (ideal for chilli)
        - Nitrogen: 110 - 135 mg/kg
        - Phosphorus: 40 - 55 mg/kg
        - Potassium: 70 - 95 mg/kg
        - Temperature: 27°C - 33°C
        - Humidity: 55% - 75%
        - Rain: False (occasionally True in monsoon demo)
        """
        # Time-based oscillation
        now = datetime.utcnow()
        hour_factor = math.sin((now.hour / 24.0) * 2 * math.pi)

        temp = round(29.0 + (hour_factor * 3.5) + random.uniform(-0.5, 0.5), 1)
        humidity = round(65.0 - (hour_factor * 8.0) + random.uniform(-2.0, 2.0), 1)
        moisture = round(44.0 + random.uniform(-3.0, 3.0), 1)
        ph = round(6.4 + random.uniform(-0.15, 0.15), 2)
        n = round(122.0 + random.uniform(-5.0, 5.0), 1)
        p = round(46.0 + random.uniform(-3.0, 3.0), 1)
        k = round(82.0 + random.uniform(-4.0, 4.0), 1)

        return {
            "device_id": device_id,
            "soil_moisture": moisture,
            "ph": ph,
            "nitrogen": n,
            "phosphorus": p,
            "potassium": k,
            "temperature": temp,
            "humidity": humidity,
            "rain_detected": False,
            "is_demo": True,
            "timestamp": now
        }

    @classmethod
    def record_sensor_data(cls, data: SensorDataInput, db: Session) -> SensorData:
        """Store incoming ESP32 or simulation payload into database"""
        record = SensorData(
            device_id=data.device_id,
            soil_moisture=data.soil_moisture,
            ph=data.ph,
            nitrogen=data.nitrogen,
            phosphorus=data.phosphorus,
            potassium=data.potassium,
            temperature=data.temperature,
            humidity=data.humidity,
            rain_detected=data.rain_detected,
            is_demo=data.is_demo if data.is_demo is not None else False,
            timestamp=datetime.utcnow()
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @classmethod
    def get_latest_telemetry(cls, db: Session) -> Dict[str, Any]:
        """
        Demo mode  -> simulated readings.
        Live mode  -> newest reading POSTed by the real ESP8266/ESP32 (is_demo = False).
        """
        if cls._demo_mode:
            latest_record = db.query(SensorData).filter(SensorData.is_demo == True)\
                .order_by(desc(SensorData.timestamp)).first()  # noqa: E712
            sim_data = cls.generate_simulated_reading()
            if not latest_record or (datetime.utcnow() - latest_record.timestamp).total_seconds() > 300:
                record = SensorData(**sim_data)
                db.add(record)
                db.commit()
                db.refresh(record)
                latest_record = record
            else:
                sim_data["id"] = 0
                latest_record = SensorData(**sim_data)
            mode = "demo"
        else:
            latest_record = db.query(SensorData).filter(SensorData.is_demo == False)\
                .order_by(desc(SensorData.timestamp)).first()  # noqa: E712
            if latest_record:
                mode = "live"
            else:
                # Live mode but the device hasn't sent anything yet
                sim_data = cls.generate_simulated_reading()
                sim_data["id"] = 0
                latest_record = SensorData(**sim_data)
                mode = "waiting"

        sm = latest_record.soil_moisture
        if sm is None:
            moisture_status = "No data"
        elif sm < 30:
            moisture_status = "Dry - Irrigation Needed"
        elif sm <= 60:
            moisture_status = "Optimal Moisture"
        else:
            moisture_status = "High / Saturated"

        ph_val = latest_record.ph
        if ph_val is None:
            ph_status = "pH not available"
        elif ph_val < 6.0:
            ph_status = "Acidic - Lime Recommended"
        elif ph_val <= 7.2:
            ph_status = "Optimal for Chilli (6.0 - 7.0)"
        else:
            ph_status = "Alkaline - Gypsum Recommended"

        if latest_record.nitrogen is None:
            npk_status = "NPK sensor not connected"
        else:
            npk_status = (f"NPK (N:{latest_record.nitrogen:.0f} "
                          f"P:{(latest_record.phosphorus or 0):.0f} K:{(latest_record.potassium or 0):.0f})")

        rain_status = "Rain Detected" if latest_record.rain_detected else "No Rain"
        if latest_record.temperature is None or latest_record.humidity is None:
            th_status = "Temperature/Humidity not available"
        else:
            th_status = f"Normal Field Conditions ({latest_record.temperature:.1f}°C, {latest_record.humidity:.1f}%)"

        return {
            "mode": mode,
            "device_id": latest_record.device_id,
            "latest": latest_record,
            "moisture_status": moisture_status,
            "ph_status": ph_status,
            "npk_status": npk_status,
            "temp_humidity_status": th_status,
            "rain_status": rain_status,
            "battery_level": 94,
            "signal_strength_dbm": -62,
            "last_updated": latest_record.timestamp or datetime.utcnow()
        }

    @classmethod
    def get_telemetry_history(cls, db: Session, hours: int = 24, limit: int = 50) -> List[SensorData]:
        """Fetch historical time-series sensor telemetry for graphs"""
        cutoff = datetime.utcnow() - timedelta(hours=hours)
        records = db.query(SensorData).filter(
            SensorData.timestamp >= cutoff,
            SensorData.is_demo == cls._demo_mode
        ).order_by(SensorData.timestamp.desc()).limit(limit).all()
        records.reverse()  # newest `limit` rows, oldest first for charts

        # Only in demo mode: synthesize trend points if history is sparse
        if cls._demo_mode and len(records) < 10:
            now = datetime.utcnow()
            for i in range(12, 0, -1):
                past_time = now - timedelta(hours=i * 2)
                hf = math.sin(((past_time.hour) / 24.0) * 2 * math.pi)
                records.append(SensorData(
                    id=i,
                    device_id="ESP32_DEMO_01",
                    soil_moisture=round(42.0 + math.cos(i) * 6.0, 1),
                    ph=round(6.4 + (i % 3) * 0.1, 2),
                    nitrogen=round(120.0 + (i % 5) * 3, 1),
                    phosphorus=round(45.0 + (i % 4) * 2, 1),
                    potassium=round(80.0 + (i % 3) * 3, 1),
                    temperature=round(28.5 + (hf * 4.0), 1),
                    humidity=round(66.0 - (hf * 9.0), 1),
                    rain_detected=False,
                    is_demo=True,
                    timestamp=past_time
                ))
            records.sort(key=lambda r: r.timestamp)

        return records
