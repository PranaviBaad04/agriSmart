"""
Water pump command state (dashboard -> backend -> ESP8266).

The dashboard sets the DESIRED state. The ESP polls it every ~2 s and reports
its ACTUAL relay state inside each sensor POST.

Safety:
  * State is kept in memory only, so a backend restart means pump = OFF.
  * When the pump is switched ON it auto-expires after MAX_RUN_SECONDS.
  * When the ESP reboots it asks the backend to reset the command to OFF.
"""
import time
from typing import Optional, Dict, Any


class PumpService:
    MAX_RUN_SECONDS = 30 * 60      # auto-off after 30 minutes (change if needed)
    DEVICE_TIMEOUT_SECONDS = 20    # ESP considered offline if silent this long

    _desired: str = "OFF"
    _on_until: Optional[float] = None
    _actual: Optional[bool] = None
    _actual_at: Optional[float] = None

    @classmethod
    def _expire_if_needed(cls):
        if cls._desired == "ON" and cls._on_until and time.time() >= cls._on_until:
            cls._desired = "OFF"
            cls._on_until = None

    @classmethod
    def set_desired(cls, state: str) -> Dict[str, Any]:
        cls._desired = state
        cls._on_until = time.time() + cls.MAX_RUN_SECONDS if state == "ON" else None
        return cls.status()

    @classmethod
    def get_command(cls, boot: bool = False) -> str:
        if boot:  # ESP just rebooted: never resume an old ON command
            cls._desired = "OFF"
            cls._on_until = None
        cls._expire_if_needed()
        return cls._desired

    @classmethod
    def report_actual(cls, pump_on: bool):
        cls._actual = bool(pump_on)
        cls._actual_at = time.time()

    @classmethod
    def status(cls) -> Dict[str, Any]:
        cls._expire_if_needed()
        age = None if cls._actual_at is None else round(time.time() - cls._actual_at, 1)
        online = age is not None and age <= cls.DEVICE_TIMEOUT_SECONDS
        remaining = None
        if cls._desired == "ON" and cls._on_until:
            remaining = max(0, int(cls._on_until - time.time()))
        return {
            "desired": cls._desired,
            "actual": None if cls._actual is None else ("ON" if cls._actual else "OFF"),
            "device_online": online,
            "last_report_age_seconds": age,
            "on_remaining_seconds": remaining,
            "max_run_minutes": cls.MAX_RUN_SECONDS // 60,
        }
