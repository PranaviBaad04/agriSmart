"""
Crop Recommendation Service: Agronomic Multi-Factor Suitability Engine
"""
from typing import Dict, Any, List
from backend.app.schemas.common import CropRecommendationInput


# Comprehensive Agro-Climatic Knowledge Base
CROPS_DATABASE = [
    {
        "name": "Chilli (मिरची)",
        "marathi_name": "मिरची (Chilli)",
        "category": "Cash / Vegetable Crop",
        "seasons": ["Kharif", "Rabi", "Zaid / Summer"],
        "min_ph": 6.0, "max_ph": 7.5,
        "ideal_n": (100, 150), "ideal_p": (35, 60), "ideal_k": (60, 110),
        "temp_range": (20, 35),
        "rainfall_range": (600, 1200),
        "soil_types": ["Loamy", "Sandy Loam / Loamy", "Black Cotton / Loamy", "Red Loamy"],
        "duration_days": "150 - 180 days",
        "expected_yield": "8 - 12 quintals (dry) / 60 - 80 q (green) per acre",
        "water_req": "Moderate (Drip irrigation recommended)",
        "ideal_ph_text": "6.0 - 7.2",
        "reasons_en": [
            "Soil pH and fertility profile provide optimal conditions for high capsaicin synthesis.",
            "Well-suited for the selected season and thermal profile with good drainage."
        ],
        "reasons_mr": [
            "जमिनीचा सामू आणि अन्नद्रव्यांचे प्रमाण तिखटपणा आणि उत्पादनासाठी अत्यंत अनुकूल आहे.",
            "निवडलेल्या हंगामातील हवामान आणि पाण्याचा निचरा मिरचीसाठी योग्य आहे."
        ]
    },
    {
        "name": "Cotton (कापूस)",
        "marathi_name": "कापूस (Cotton)",
        "category": "Cash / Commercial Fiber",
        "seasons": ["Kharif"],
        "min_ph": 6.5, "max_ph": 8.5,
        "ideal_n": (110, 160), "ideal_p": (40, 70), "ideal_k": (60, 120),
        "temp_range": (22, 36),
        "rainfall_range": (500, 1000),
        "soil_types": ["Black Cotton / Loamy", "Clay Loam"],
        "duration_days": "160 - 200 days",
        "expected_yield": "10 - 15 quintals per acre",
        "water_req": "Moderate to High",
        "ideal_ph_text": "6.5 - 8.0",
        "reasons_en": [
            "Deep black soil and warm temperatures are ideal for boll development.",
            "High nutrient responsiveness and favorable moisture retention."
        ],
        "reasons_mr": [
            "काळी कसदार जमीन आणि उबदार हवामान कापसाच्या बोंडांच्या वाढीसाठी उत्तम आहे.",
            "जमिनीची ओलावा टिकवून ठेवण्याची क्षमता कापसाला अनुकूल आहे."
        ]
    },
    {
        "name": "Soybean (सोयाबीन)",
        "marathi_name": "सोयाबीन (Soybean)",
        "category": "Oilseed / Legume",
        "seasons": ["Kharif"],
        "min_ph": 6.0, "max_ph": 7.5,
        "ideal_n": (60, 100), "ideal_p": (40, 70), "ideal_k": (50, 90),
        "temp_range": (20, 32),
        "rainfall_range": (600, 900),
        "soil_types": ["Black Cotton / Loamy", "Loamy", "Clay Loam"],
        "duration_days": "90 - 105 days",
        "expected_yield": "10 - 14 quintals per acre",
        "water_req": "Moderate",
        "ideal_ph_text": "6.0 - 7.5",
        "reasons_en": [
            "Biological nitrogen-fixing legume, enriching soil health.",
            "Short duration with reliable market liquidity and low nitrogen requirement."
        ],
        "reasons_mr": [
            "मुळांमधील गाठींमुळे हवेतील नत्र जमिनीत स्थिर करते आणि जमीन सुपीक बनवते.",
            "कमी कालावधीचे पीक असून कमी खर्चात चांगला नफा मिळतो."
        ]
    },
    {
        "name": "Onion (कांदा)",
        "marathi_name": "कांदा (Onion)",
        "category": "Horticultural Cash Crop",
        "seasons": ["Kharif", "Rabi", "Late Kharif"],
        "min_ph": 6.0, "max_ph": 7.8,
        "ideal_n": (100, 140), "ideal_p": (45, 75), "ideal_k": (75, 120),
        "temp_range": (15, 30),
        "rainfall_range": (500, 800),
        "soil_types": ["Sandy Loam / Loamy", "Loamy", "Red Loamy"],
        "duration_days": "120 - 140 days",
        "expected_yield": "100 - 150 quintals per acre",
        "water_req": "Moderate with regular light intervals",
        "ideal_ph_text": "6.0 - 7.5",
        "reasons_en": [
            "High potassium and phosphorus levels support firm bulb enlargement.",
            "Excellent returns in well-drained loamy soils during Rabi and Kharif."
        ],
        "reasons_mr": [
            "जमिनीतील पोटॅश आणि स्फुरद कांद्याची फुगवण आणि साठवणूक क्षमता वाढवतात.",
            "पाण्याचा उत्तम निचरा होणाऱ्या जमिनीत कांद्याचे भरघोस उत्पादन मिळते."
        ]
    },
    {
        "name": "Chickpea / Bengal Gram (हरभरा)",
        "marathi_name": "हरभरा (Gram / Chana)",
        "category": "Rabi Pulse",
        "seasons": ["Rabi"],
        "min_ph": 6.0, "max_ph": 8.0,
        "ideal_n": (40, 80), "ideal_p": (40, 60), "ideal_k": (40, 80),
        "temp_range": (12, 28),
        "rainfall_range": (400, 700),
        "soil_types": ["Black Cotton / Loamy", "Loamy", "Clay Loam"],
        "duration_days": "100 - 120 days",
        "expected_yield": "8 - 12 quintals per acre",
        "water_req": "Low to Moderate (1-2 protective irrigations)",
        "ideal_ph_text": "6.0 - 7.8",
        "reasons_en": [
            "Low water requirement; thrives on residual soil moisture during winter Rabi.",
            "High market demand with low fertilizer input costs."
        ],
        "reasons_mr": [
            "कमी पाण्यात येणारे रब्बीतील उत्तम कडधान्य पीक.",
            "खतांचा खर्च कमी आणि जमिनीत ओलावा असताना उत्तम उत्पादन."
        ]
    },
    {
        "name": "Tomato (टोमॅटो)",
        "marathi_name": "टोमॅटो (Tomato)",
        "category": "Vegetable Crop",
        "seasons": ["Kharif", "Rabi", "Zaid / Summer"],
        "min_ph": 6.0, "max_ph": 7.5,
        "ideal_n": (110, 160), "ideal_p": (50, 80), "ideal_k": (80, 140),
        "temp_range": (18, 32),
        "rainfall_range": (500, 1000),
        "soil_types": ["Sandy Loam / Loamy", "Loamy", "Red Loamy"],
        "duration_days": "120 - 150 days",
        "expected_yield": "200 - 300 quintals per acre",
        "water_req": "Moderate (Drip with mulching)",
        "ideal_ph_text": "6.0 - 7.0",
        "reasons_en": [
            "High nutrient responsiveness and high productivity under drip fertigation.",
            "Favorable temperature and soil aeration promote heavy fruit setting."
        ],
        "reasons_mr": [
            "ठिबक सिंचनावर भरघोस उत्पादन देणारे भाजीपाला पीक.",
            "जमिनीची सुपीकता आणि हवामान टोमॅटोच्या उत्तम फळधारणेस पोषक आहे."
        ]
    }
]


class CropService:

    @classmethod
    def recommend_crops(cls, data: CropRecommendationInput) -> Dict[str, Any]:
        scored_crops = []

        for crop in CROPS_DATABASE:
            score = 70  # Baseline

            # 1. Season Match
            if data.season in crop["seasons"]:
                score += 15
            else:
                score -= 20

            # 2. pH Match
            if crop["min_ph"] <= data.ph <= crop["max_ph"]:
                score += 10
            else:
                score -= 15

            # 3. NPK Matching
            if crop["ideal_n"][0] <= data.nitrogen <= crop["ideal_n"][1] + 30:
                score += 5
            if crop["ideal_p"][0] <= data.phosphorus <= crop["ideal_p"][1] + 20:
                score += 5
            if crop["ideal_k"][0] <= data.potassium <= crop["ideal_k"][1] + 30:
                score += 5

            # 4. Soil Type Match
            if any(st.lower() in data.soil_type.lower() for st in crop["soil_types"]):
                score += 5

            score = min(max(score, 35), 98)

            scored_crops.append({
                "crop_name": crop["name"],
                "marathi_name": crop["marathi_name"],
                "suitability_score": score,
                "category": crop["category"],
                "duration_days": crop["duration_days"],
                "expected_yield_per_acre": crop["expected_yield"],
                "water_requirement": crop["water_req"],
                "soil_ph_ideal": crop["ideal_ph_text"],
                "reasons_en": crop["reasons_en"],
                "reasons_mr": crop["reasons_mr"]
            })

        # Sort by suitability descending
        scored_crops.sort(key=lambda c: c["suitability_score"], reverse=True)
        top_crop = scored_crops[0]["crop_name"]

        return {
            "recommended_crops": scored_crops,
            "primary_recommendation": top_crop,
            "soil_suitability_summary": f"Based on your soil pH ({data.ph}) and {data.season} season, {top_crop} demonstrates the highest agronomic compatibility.",
            "input_parameters": data.dict()
        }
