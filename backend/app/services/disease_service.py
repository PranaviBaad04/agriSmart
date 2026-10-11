"""
Disease Service: Integrates Cloudinary, PyTorch Model Inference, and Database Logging
"""
import sys
from pathlib import Path
from typing import Dict, Any
from sqlalchemy.orm import Session

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(ROOT_DIR))

try:
    from ml.predict import ChilliDiseasePredictor
except ImportError:  # ml/ folder not present: disease detection disabled, IoT etc. still work
    ChilliDiseasePredictor = None
from backend.app.services.cloudinary_service import upload_image, validate_image_file
from backend.app.database.models import DiseaseDetection


class DiseaseService:
    _predictor = None

    @classmethod
    def get_predictor(cls):
        if ChilliDiseasePredictor is None:
            raise RuntimeError(
                "Disease model code (the 'ml' folder) is missing, so disease detection is unavailable."
            )
        if cls._predictor is None:
            cls._predictor = ChilliDiseasePredictor()
        return cls._predictor

    @classmethod
    def predict_and_store(
        cls,
        file_bytes: bytes,
        filename: str,
        db: Session,
        user_id: int = None
    ) -> Dict[str, Any]:
        """
        Complete pipeline:
        1. Validate file
        2. Upload to Cloudinary (or local fallback)
        3. Preprocess and run PyTorch Deep Learning Inference
        4. Calculate Prototype Severity Estimation
        5. Generate Agronomic Recommendations
        6. Persist record in database
        7. Return structured JSON
        """
        # 1. Validation
        is_valid, msg = validate_image_file(filename, file_bytes)
        if not is_valid:
            raise ValueError(msg)

        # 2. Upload to Cloudinary
        upload_result = upload_image(
            file_bytes=file_bytes,
            original_filename=filename,
            folder="AgriSmart/chilli/disease-detection"
        )
        image_url = upload_result["image_url"]
        public_id = upload_result.get("public_id")

        # 3. Model Inference & Severity Analysis
        predictor = cls.get_predictor()
        prediction_result = predictor.predict(file_bytes)

        # 4. Format primary recommendation text
        primary_rec = "\n".join(prediction_result["recommendations"]["en"])

        # 5. Persist to Database
        db_record = DiseaseDetection(
            user_id=user_id,
            crop="Chilli (Capsicum annuum)",
            image_url=image_url,
            cloudinary_public_id=public_id,
            disease=prediction_result["disease"],
            confidence=prediction_result["confidence"],
            severity=prediction_result["severity"],
            severity_level=prediction_result["severity_level"],
            lesion_coverage_percent=prediction_result["lesion_coverage_percent"],
            recommendation=primary_rec
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)

        return {
            "id": db_record.id,
            "crop": db_record.crop,
            "disease": prediction_result["disease"],
            "disease_display_name": prediction_result["disease_display_name"],
            "scientific_name": prediction_result["scientific_name"],
            "confidence": prediction_result["confidence"],
            "severity": prediction_result["severity"],
            "severity_level": prediction_result["severity_level"],
            "lesion_coverage_percent": prediction_result["lesion_coverage_percent"],
            "severity_method": prediction_result["severity_method"],
            "recommendation": primary_rec,
            "description": prediction_result["description"],
            "recommendations_list": prediction_result["recommendations"],
            "all_probabilities": prediction_result["all_probabilities"],
            "image_url": image_url,
            "cloudinary_public_id": public_id,
            "created_at": db_record.created_at
        }
