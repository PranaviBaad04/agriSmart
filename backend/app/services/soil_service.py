"""
Soil Health Analysis Service: NPK, pH & Organic Carbon Diagnostic Engine
"""
from datetime import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from backend.app.database.models import SoilRecord
from backend.app.schemas.common import SoilAnalysisInput, NutrientRating, SoilAnalysisResult


class SoilService:

    @classmethod
    def evaluate_ph(cls, ph: float) -> NutrientRating:
        if ph < 5.5:
            return NutrientRating(
                value=ph, unit="pH", status="Deficient (Strongly Acidic)",
                optimal_range="6.0 - 7.0",
                advice_en="Apply agricultural lime (calcium carbonate) or dolomite to raise soil pH.",
                advice_mr="जमिनीचा आम्लधर्मीपणा कमी करण्यासाठी कृषी चुना किंवा डोलोमाइट वापरा."
            )
        elif ph < 6.0:
            return NutrientRating(
                value=ph, unit="pH", status="Low (Moderately Acidic)",
                optimal_range="6.0 - 7.0",
                advice_en="Incorporate well-rotted farmyard manure and light calcitic lime.",
                advice_mr="शेणखत आणि हलका चुना मिसळून जमिनीचा पोत सुधारा."
            )
        elif ph <= 7.2:
            return NutrientRating(
                value=ph, unit="pH", status="Optimal (Ideal for Chilli)",
                optimal_range="6.0 - 7.0",
                advice_en="Soil pH is ideal for nutrient bioavailability and root absorption.",
                advice_mr="जमिनीचा सामू मिरची पिकासाठी अत्यंत उत्तम आहे."
            )
        elif ph <= 8.2:
            return NutrientRating(
                value=ph, unit="pH", status="High (Moderately Alkaline)",
                optimal_range="6.0 - 7.0",
                advice_en="Apply elemental sulphur or gypsum (calcium sulphate) and organic compost.",
                advice_mr="क्षारयुक्तता कमी करण्यासाठी जिप्सम किंवा गंधक आणि सेंद्रिय खत वापरा."
            )
        else:
            return NutrientRating(
                value=ph, unit="pH", status="Deficient (Strongly Alkaline/Saline)",
                optimal_range="6.0 - 7.0",
                advice_en="Heavy gypsum treatment required with leaching and green manuring (dhaincha).",
                advice_mr="जिप्समचा मोठा डोस द्या आणि धैंचा/ताग गाडून हिरवळीचे खत करा."
            )

    @classmethod
    def evaluate_nitrogen(cls, n: float) -> NutrientRating:
        if n < 90:
            return NutrientRating(
                value=n, unit="mg/kg", status="Deficient",
                optimal_range="110 - 150 mg/kg",
                advice_en="Severe nitrogen deficiency. Apply neem-coated urea or ammonium sulphate in split doses.",
                advice_mr="नायट्रोजनची तीव्र कमतरता आहे. युरिया खताची विभागून मात्रा द्या."
            )
        elif n < 110:
            return NutrientRating(
                value=n, unit="mg/kg", status="Low",
                optimal_range="110 - 150 mg/kg",
                advice_en="Moderate nitrogen deficiency. Supplement with vermicompost and balanced fertigation.",
                advice_mr="नायट्रोजन कमी आहे. गांडूळ खत आणि १९:१९:१९ चा वापर करा."
            )
        elif n <= 160:
            return NutrientRating(
                value=n, unit="mg/kg", status="Optimal",
                optimal_range="110 - 150 mg/kg",
                advice_en="Nitrogen levels are optimal for vegetative and branching vigor.",
                advice_mr="नायट्रोजनचे प्रमाण झाडाच्या चांगल्या वाढीसाठी योग्य आहे."
            )
        else:
            return NutrientRating(
                value=n, unit="mg/kg", status="High",
                optimal_range="110 - 150 mg/kg",
                advice_en="Excess nitrogen causes rank vegetative growth and pest vulnerability. Reduce urea applications.",
                advice_mr="जास्त नायट्रोजनमुळे झाडांची अनावश्यक वाढ होते आणि कीड वाढते. युरिया कमी करा."
            )

    @classmethod
    def evaluate_phosphorus(cls, p: float) -> NutrientRating:
        if p < 25:
            return NutrientRating(
                value=p, unit="mg/kg", status="Deficient",
                optimal_range="35 - 55 mg/kg",
                advice_en="Low phosphorus restricts root development and flower set. Apply Single Super Phosphate (SSP) or DAP.",
                advice_mr="स्फुरदची कमतरता आहे. मुळांच्या वाढीसाठी सिंगल सुपर फॉस्फेट (SSP) किंवा DAP द्या."
            )
        elif p < 35:
            return NutrientRating(
                value=p, unit="mg/kg", status="Low",
                optimal_range="35 - 55 mg/kg",
                advice_en="Supplement with Phosphorus Solubilizing Bacteria (PSB) biofertilizer.",
                advice_mr="जमिनीतील स्फुरद विरघळवण्यासाठी पी.एस.बी. (PSB) जिवाणू खत वापरा."
            )
        elif p <= 65:
            return NutrientRating(
                value=p, unit="mg/kg", status="Optimal",
                optimal_range="35 - 55 mg/kg",
                advice_en="Phosphorus is optimal for profuse root establishment and flower retention.",
                advice_mr="स्फुरदचे प्रमाण फुलोरा आणि मुळांच्या मजबुतीसाठी उत्तम आहे."
            )
        else:
            return NutrientRating(
                value=p, unit="mg/kg", status="High",
                optimal_range="35 - 55 mg/kg",
                advice_en="High phosphorus can lock micronutrients like Zinc and Iron. Hold phosphate fertilizers.",
                advice_mr="जास्त स्फुरदमुळे जस्त आणि लोह मिळण्यात अडथळा येतो. फॉस्फेट खते देणे टाळा."
            )

    @classmethod
    def evaluate_potassium(cls, k: float) -> NutrientRating:
        if k < 50:
            return NutrientRating(
                value=k, unit="mg/kg", status="Deficient",
                optimal_range="70 - 110 mg/kg",
                advice_en="Potassium deficiency weakens disease immunity and fruit quality. Apply Muriate of Potash (MOP) or SOP.",
                advice_mr="पोटॅशची कमतरता आहे. फळांची प्रत आणि रोगप्रतिकारशक्तीसाठी पोटॅश (MOP/SOP) द्या."
            )
        elif k < 70:
            return NutrientRating(
                value=k, unit="mg/kg", status="Low",
                optimal_range="70 - 110 mg/kg",
                advice_en="Apply potassium sulphate (0:0:50) foliar spray during chilli fruit setting.",
                advice_mr="फळधारणेच्या काळात ००:००:५० खताची फवारणी करा."
            )
        elif k <= 120:
            return NutrientRating(
                value=k, unit="mg/kg", status="Optimal",
                optimal_range="70 - 110 mg/kg",
                advice_en="Potassium level is optimal, supporting high pungency and thick-walled pods.",
                advice_mr="पोटॅशचे प्रमाण मिरचीच्या चमकदार रंगासाठी आणि वजनासाठी परिपूर्ण आहे."
            )
        else:
            return NutrientRating(
                value=k, unit="mg/kg", status="High",
                optimal_range="70 - 110 mg/kg",
                advice_en="High potassium. Maintain current regime without additional potash.",
                advice_mr="पोटॅशचे प्रमाण पुरेसे आहे, अतिरिक्त पोटॅश देऊ नका."
            )

    @classmethod
    def evaluate_organic_carbon(cls, oc: float) -> NutrientRating:
        if oc < 0.5:
            return NutrientRating(
                value=oc, unit="%", status="Deficient",
                optimal_range="0.75 - 1.25%",
                advice_en="Low soil organic matter. Apply 5 tons/acre well-decomposed FYM or compost.",
                advice_mr="सेंद्रिय कर्ब खूप कमी आहे. एकरी ५ टन शेणखत किंवा कंपोस्ट खत टाका."
            )
        elif oc < 0.75:
            return NutrientRating(
                value=oc, unit="%", status="Low",
                optimal_range="0.75 - 1.25%",
                advice_en="Incorporate green manuring and crop residue mulching.",
                advice_mr="ताग/धैंचा गाडून हिरवळीचे खत करा आणि सेंद्रिय आच्छादन वापरा."
            )
        elif oc <= 1.3:
            return NutrientRating(
                value=oc, unit="%", status="Optimal",
                optimal_range="0.75 - 1.25%",
                advice_en="Excellent organic matter promoting healthy soil microbial microbiome.",
                advice_mr="सेंद्रिय कर्ब उत्तम आहे, ज्यामुळे जमिनीची सुपीकता टिकून राहते."
            )
        else:
            return NutrientRating(
                value=oc, unit="%", status="High",
                optimal_range="0.75 - 1.25%",
                advice_en="High organic matter content.",
                advice_mr="सेंद्रिय कर्बाचे प्रमाण भरपूर आहे."
            )

    @classmethod
    def analyze_soil(cls, data: SoilAnalysisInput, db: Session = None) -> Dict[str, Any]:
        ph_r = cls.evaluate_ph(data.ph)
        n_r = cls.evaluate_nitrogen(data.nitrogen)
        p_r = cls.evaluate_phosphorus(data.phosphorus)
        k_r = cls.evaluate_potassium(data.potassium)
        oc_r = cls.evaluate_organic_carbon(data.organic_carbon or 0.65)

        # Health score calculation
        score = 100
        for r in [ph_r, n_r, p_r, k_r, oc_r]:
            if "Deficient" in r.status:
                score -= 18
            elif "Low" in r.status or "High" in r.status:
                score -= 8

        score = max(min(score, 100), 20)
        overall_status = "Optimal / Highly Fertile" if score >= 80 else ("Moderate Fertility" if score >= 60 else "Nutrient Stressed / Low Fertility")

        recs_en = [
            f"pH ({data.ph}): {ph_r.advice_en}",
            f"Nitrogen ({data.nitrogen} mg/kg): {n_r.advice_en}",
            f"Phosphorus ({data.phosphorus} mg/kg): {p_r.advice_en}",
            f"Potassium ({data.potassium} mg/kg): {k_r.advice_en}",
            f"Organic Carbon ({data.organic_carbon}%): {oc_r.advice_en}"
        ]

        recs_mr = [
            f"सामू (pH {data.ph}): {ph_r.advice_mr}",
            f"नायट्रोजन ({data.nitrogen} mg/kg): {n_r.advice_mr}",
            f"स्फुरद ({data.phosphorus} mg/kg): {p_r.advice_mr}",
            f"पोटॅश ({data.potassium} mg/kg): {k_r.advice_mr}",
            f"सेंद्रिय कर्ब ({data.organic_carbon}%): {oc_r.advice_mr}"
        ]

        if db:
            record = SoilRecord(
                sample_name=data.sample_name or "Plot A",
                ph=data.ph,
                nitrogen=data.nitrogen,
                phosphorus=data.phosphorus,
                potassium=data.potassium,
                organic_carbon=data.organic_carbon or 0.65,
                overall_status=overall_status,
                recommendations="\n".join(recs_en)
            )
            db.add(record)
            db.commit()

        return {
            "sample_name": data.sample_name or "Plot A",
            "ph_rating": ph_r.dict(),
            "nitrogen_rating": n_r.dict(),
            "phosphorus_rating": p_r.dict(),
            "potassium_rating": k_r.dict(),
            "organic_carbon_rating": oc_r.dict(),
            "overall_health_score": score,
            "overall_status": overall_status,
            "fertilizer_recommendations_en": recs_en,
            "fertilizer_recommendations_mr": recs_mr,
            "created_at": datetime.utcnow()
        }
