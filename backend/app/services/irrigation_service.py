"""
Smart Irrigation Service: Rule-Based Agronomic Water Balance Model
"""
from datetime import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.app.database.models import IrrigationRecommendation
from backend.app.schemas.common import IrrigationCalculationInput, IrrigationAdviceResult


class IrrigationService:

    @classmethod
    def calculate_irrigation_advice(
        cls,
        data: IrrigationCalculationInput,
        db: Session = None
    ) -> Dict[str, Any]:
        """
        Evaluate soil water tension, evapotranspiration factors, and precipitation forecasts.
        """
        sm = data.soil_moisture
        temp = data.temperature or 30.0
        humidity = data.humidity or 60.0
        rain_detected = data.rain_detected or False
        rain_prob = data.rain_probability_next_24h or 0
        stage = data.crop_growth_stage

        # Stage water factor
        stage_water_multiplier = {
            "Vegetative / Seedling": 0.75,
            "Flowering & Fruit Development": 1.25,
            "Fruit Ripening & Harvesting": 0.85
        }.get(stage, 1.0)

        # 1. Rain Scenario
        if rain_detected or rain_prob >= 75:
            advice = {
                "irrigation_required": False,
                "urgency_level": "Not Needed",
                "water_requirement_liters_per_acre": 0,
                "recommended_duration_minutes": 0,
                "recommended_timing": "Postpone Irrigation",
                "reason_en": f"Rainfall detected or high precipitation probability ({rain_prob}%). Natural rainfall will meet crop water requirements.",
                "reason_mr": f"पाऊस सुरू आहे किंवा पावसाची शक्यता जास्त आहे ({rain_prob}%). सिंचन पुढे ढकला, नैसर्गिक पाऊस पिकाची गरज पूर्ण करेल.",
                "action_items_en": [
                    "Ensure field drainage channels are clear to prevent root waterlogging.",
                    "Pause automated drip fertigation cycles.",
                    "Monitor soil moisture 12 hours post-rain."
                ],
                "action_items_mr": [
                    "मुळांभोवती पाणी साचू नये म्हणून शेतातील पाण्याचा निचरा नीट ठेवा.",
                    "ठिबक सिंचन आणि खतांचा डोस सध्या थांबवा.",
                    "पाऊस थांबल्यानंतर १२ तासांनी पुन्हा ओलावा तपासा."
                ]
            }
        # 2. Critical Dry (< 30%)
        elif sm < 30.0:
            base_liters = int(14000 * stage_water_multiplier)
            duration_mins = int(90 * stage_water_multiplier)
            advice = {
                "irrigation_required": True,
                "urgency_level": "Immediate",
                "water_requirement_liters_per_acre": base_liters,
                "recommended_duration_minutes": duration_mins,
                "recommended_timing": "Early Morning (6:00 AM - 8:30 AM) or Evening (5:30 PM)",
                "reason_en": f"Soil moisture is critically low ({sm:.1f}%). Chilli plants are approaching permanent wilting point at {stage} stage.",
                "reason_mr": f"जमिनीतील ओलावा अत्यंत कमी आहे ({sm:.1f}%). {stage} या संवेदनशील टप्प्यावर पिकाला त्वरित पाण्याची गरज आहे.",
                "action_items_en": [
                    "Start drip irrigation immediately for the recommended duration.",
                    "Avoid high-noon watering to minimize evaporative losses.",
                    "Check drip emitters for uniform water discharge."
                ],
                "action_items_mr": [
                    "तातडीने ठिबक सिंचन सुरू करा.",
                    "दुपारी कडक उन्हात पाणी देणे टाळा, सकाळी किंवा संध्याकाळी पाणी द्या.",
                    "ठिबकचे ड्रिपर्स तुंबले नाहीत ना याची खात्री करा."
                ]
            }
        # 3. Moderate / Depleting (30% - 48%)
        elif sm <= 48.0:
            base_liters = int(8500 * stage_water_multiplier)
            duration_mins = int(50 * stage_water_multiplier)
            advice = {
                "irrigation_required": True,
                "urgency_level": "Scheduled",
                "water_requirement_liters_per_acre": base_liters,
                "recommended_duration_minutes": duration_mins,
                "recommended_timing": "Tomorrow Morning (6:30 AM - 8:00 AM)",
                "reason_en": f"Soil moisture ({sm:.1f}%) is in depletion zone. Scheduled irrigation will sustain vegetative vigor without root stress.",
                "reason_mr": f"जमिनीतील ओलावा कमी होत आहे ({sm:.1f}%). पिकाची चांगली वाढ टिकवण्यासाठी वेळेवर सिंचन करा.",
                "action_items_en": [
                    "Schedule light drip irrigation during cooler morning hours.",
                    "Fertigation with water-soluble fertilizers can be integrated.",
                    "Apply straw/organic mulch to retain soil moisture."
                ],
                "action_items_mr": [
                    "उद्या सकाळी हलके पाणी द्या.",
                    "पाण्यासोबत विद्राव्य खतांचा डोस (फर्टिगेशन) देऊ शकता.",
                    "ओलावा टिकवण्यासाठी आच्छादन (मल्चिंग) चा वापर करा."
                ]
            }
        # 4. Optimal Moisture (48% - 70%)
        elif sm <= 70.0:
            advice = {
                "irrigation_required": False,
                "urgency_level": "Not Needed",
                "water_requirement_liters_per_acre": 0,
                "recommended_duration_minutes": 0,
                "recommended_timing": "No Irrigation Required",
                "reason_en": f"Soil moisture ({sm:.1f}%) is in the optimal root-zone range for Chilli. Crop transpiration is well-supported.",
                "reason_mr": f"जमिनीतील ओलावा ({sm:.1f}%) मिरची पिकासाठी अत्यंत योग्य आहे. सध्या पाणी देण्याची गरज नाही.",
                "action_items_en": [
                    "Maintain current soil condition.",
                    "Re-evaluate sensor telemetry in 24 hours.",
                    "Perform routine weed inspection."
                ],
                "action_items_mr": [
                    "सध्याची परिस्थिती उत्तम आहे, पाणी देणे टाळा.",
                    "२४ तासांनंतर पुन्हा सेन्सर डेटा तपासा.",
                    "शेतातील तण नियंत्रण करा."
                ]
            }
        # 5. Excess Moisture (> 70%)
        else:
            advice = {
                "irrigation_required": False,
                "urgency_level": "Excess Moisture Warning",
                "water_requirement_liters_per_acre": 0,
                "recommended_duration_minutes": 0,
                "recommended_timing": "Stop All Irrigation",
                "reason_en": f"Soil moisture is excessively high ({sm:.1f}%). Risk of root hypoxia, damping off, and bacterial wilt.",
                "reason_mr": f"जमिनीत जास्त पाणी साचले आहे ({sm:.1f}%). मुळे कुजणे आणि मर रोगाचा धोका वाढू शकतो.",
                "action_items_en": [
                    "Suspend all irrigation immediately.",
                    "Open drainage furrows to discharge excess standing water.",
                    "Inspect roots and collar region for fungal signs."
                ],
                "action_items_mr": [
                    "सर्व प्रकारचे सिंचन त्वरित थांबवा.",
                    "शेतातून अतिरिक्त पाणी बाहेर काढण्यासाठी चारी करा.",
                    "रोपांच्या बुंध्याशी बुरशी किंवा कुजण्याची लक्षणे तपासा."
                ]
            }

        # Store to DB if session provided
        if db:
            rec = IrrigationRecommendation(
                soil_moisture=sm,
                weather_condition=f"Temp: {temp}°C, Hum: {humidity}%, RainProb: {rain_prob}%",
                crop=data.crop,
                recommendation=advice["reason_en"],
                water_level=advice["urgency_level"],
                timing=advice["recommended_timing"],
                reason=advice["reason_en"]
            )
            db.add(rec)
            db.commit()

        advice["method"] = "Rule-based Agronomic Water Balance Model"
        advice["created_at"] = datetime.utcnow()
        return advice
