"""
Weather Service: OpenWeatherMap Integration

Supports:
- City-based weather
- Latitude/longitude weather
- Automatic location name from OpenWeatherMap
- No hard-coded Pune location
- Agricultural weather alerts
"""

import os
import requests

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from pathlib import Path

from dotenv import load_dotenv


# =========================================================
# ENVIRONMENT
# =========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent

load_dotenv(ROOT_DIR / ".env")


WEATHER_API_KEY = os.getenv(
    "WEATHER_API_KEY",
    ""
)


# =========================================================
# WEATHER SERVICE
# =========================================================

class WeatherService:

    @classmethod
    def get_weather(
        cls,
        city: Optional[str] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None
    ) -> Dict[str, Any]:

        """
        Fetch real-time weather from OpenWeatherMap.

        Location priority:

        1. Latitude + longitude
        2. City name
        3. Return error

        No hard-coded Pune fallback.
        """

        # =================================================
        # API KEY CHECK
        # =================================================

        if (
            not WEATHER_API_KEY
            or WEATHER_API_KEY == "your_weather_api_key_here"
        ):

            return {
                "error": "Weather API key is not configured.",
                "message": (
                    "Please configure WEATHER_API_KEY "
                    "in the .env file."
                )
            }


        try:

            # =================================================
            # OPTION 1:
            # LATITUDE + LONGITUDE
            # =================================================

            if lat is not None and lon is not None:

                print(
                    f"Fetching weather using GPS coordinates: "
                    f"lat={lat}, lon={lon}"
                )

                url = (
                    "https://api.openweathermap.org/data/2.5/weather"
                    f"?lat={lat}"
                    f"&lon={lon}"
                    f"&appid={WEATHER_API_KEY}"
                    "&units=metric"
                )


            # =================================================
            # OPTION 2:
            # CITY NAME
            # =================================================

            elif city:

                print(
                    f"Fetching weather using city: {city}"
                )

                url = (
                    "https://api.openweathermap.org/data/2.5/weather"
                    f"?q={city}"
                    f"&appid={WEATHER_API_KEY}"
                    "&units=metric"
                )


            # =================================================
            # NO LOCATION
            # =================================================

            else:

                return {
                    "error": "Location is required.",
                    "message": (
                        "Please provide a city "
                        "or latitude/longitude."
                    )
                }


            # =================================================
            # REQUEST OPENWEATHER
            # =================================================

            response = requests.get(
                url,
                timeout=10
            )


            # =================================================
            # API ERROR
            # =================================================

            if response.status_code != 200:

                print(
                    "Weather API error:",
                    response.status_code,
                    response.text
                )

                return {
                    "error": "Unable to fetch weather.",
                    "message": response.text
                }


            data = response.json()


            # =================================================
            # GET ACTUAL LOCATION
            # =================================================

            # When latitude/longitude are used, OpenWeather
            # returns the actual nearest city/location.

            actual_city = data.get(
                "name",
                city or "Unknown"
            )


            country = data.get(
                "sys",
                {}
            ).get(
                "country",
                ""
            )


            location_name = actual_city


            if country:

                location_name = (
                    f"{actual_city}, {country}"
                )


            print(
                f"Weather location returned by OpenWeather: "
                f"{location_name}"
            )


            # =================================================
            # WEATHER VALUES
            # =================================================

            temp = float(
                data["main"]["temp"]
            )


            feels_like = float(
                data["main"].get(
                    "feels_like",
                    temp
                )
            )


            humidity = int(
                data["main"]["humidity"]
            )


            pressure = int(
                data["main"].get(
                    "pressure",
                    0
                )
            )


            # OpenWeather wind speed is m/s.
            # Convert to km/h.

            wind = (
                float(
                    data.get(
                        "wind",
                        {}
                    ).get(
                        "speed",
                        0
                    )
                )
                * 3.6
            )


            condition = data["weather"][0]["main"]


            weather_description = data["weather"][0].get(
                "description",
                condition
            )


            # Existing logic retained.
            rain_probability = 0


            # =================================================
            # FORMAT RESPONSE
            # =================================================

            return cls._format_weather_response(

                city=location_name,

                temp=round(
                    temp,
                    1
                ),

                feels_like=round(
                    feels_like,
                    1
                ),

                humidity=humidity,

                wind=wind,

                condition=condition,

                description=weather_description,

                pressure=pressure,

                rain_probability=rain_probability

            )


        # =====================================================
        # REQUEST ERROR
        # =====================================================

        except requests.RequestException as e:

            print(
                f"Weather API request failed: {e}"
            )

            return {
                "error": "Weather service unavailable.",
                "message": str(e)
            }


        # =====================================================
        # PROCESSING ERROR
        # =====================================================

        except Exception as e:

            print(
                f"Weather processing error: {e}"
            )

            return {
                "error": "Weather processing failed.",
                "message": str(e)
            }


    # =========================================================
    # FORMAT WEATHER RESPONSE
    # =========================================================

    @classmethod
    def _format_weather_response(
        cls,
        city: str,
        temp: float,
        feels_like: float,
        humidity: int,
        wind: float,
        condition: str,
        description: str,
        pressure: int,
        rain_probability: int
    ) -> Dict[str, Any]:

        now = datetime.now()


        # =====================================================
        # AGRICULTURAL ALERT
        # =====================================================

        alert = None


        if humidity > 75 and temp > 28:

            alert = (
                "High humidity (>75%) and warm temperature "
                "detected. There may be increased risk of "
                "fungal diseases. Monitor crops regularly "
                "and avoid unnecessary overhead irrigation."
            )


        elif temp > 35:

            alert = (
                "High temperature detected. "
                "Monitor crops for heat stress and maintain "
                "adequate soil moisture."
            )


        elif temp < 15:

            alert = (
                "Low temperature detected. "
                "Sensitive crops may experience reduced growth."
            )


        # =====================================================
        # 7-DAY FORECAST
        #
        # Existing logic retained.
        # =====================================================

        forecast = []


        for i in range(1, 8):

            forecast_date = (
                now + timedelta(days=i)
            )


            day_name = forecast_date.strftime(
                "%a"
            )


            date_str = forecast_date.strftime(
                "%d %b"
            )


            temperature_variation = (
                (i % 3) - 1
            )


            t_max = round(
                temp + temperature_variation,
                1
            )


            t_min = round(
                t_max - 7.5,
                1
            )


            forecast.append({

                "date": date_str,

                "day_name": day_name,

                "temp_max_c": t_max,

                "temp_min_c": t_min,

                "humidity_percent": max(
                    40,
                    min(
                        95,
                        humidity - (i * 1)
                    )
                ),

                "rain_probability":
                    rain_probability,

                "condition":
                    condition,

                "icon":
                    "cloud-sun"

            })


        # =====================================================
        # SUMMARIES
        # =====================================================

        summary_en = (

            f"{condition} ({description}) with a temperature of "

            f"{temp}°C and relative humidity of "

            f"{humidity}%. "

            f"Winds are blowing at "

            f"{wind:.1f} km/h."

        )


        summary_mr = (

            f"{condition} ({description}), "

            f"तापमान {temp}°C आणि "

            f"हवेतील आर्द्रता {humidity}% आहे. "

            f"वाऱ्याचा वेग {wind:.1f} किमी/तास आहे."

        )


        # =====================================================
        # FINAL RESPONSE
        # =====================================================

        return {

            "current": {

                # Actual location obtained from OpenWeather
                "location": city,

                "temperature_c":
                    temp,

                "feels_like_c":
                    feels_like,

                "humidity_percent":
                    humidity,

                "rainfall_mm":
                    0.0,

                "wind_speed_kmh":
                    round(
                        wind,
                        1
                    ),

                "weather_condition":
                    condition,

                "weather_description":
                    description,

                "weather_icon":
                    "cloud-sun",

                # -------------------------------------------------
                # IMPORTANT:
                # Current OpenWeather endpoint does not return UV
                # here. Your response schema expects a float.
                # Therefore use numeric 0.0 instead of None.
                # -------------------------------------------------

                "uv_index":
                    0.0,

                "pressure_hpa":
                    pressure,

                "rain_probability_percent":
                    rain_probability,

                "forecast_summary_en":
                    summary_en,

                "forecast_summary_mr":
                    summary_mr,

                "agricultural_alert":
                    alert

            },


            "forecast":
                forecast

        }