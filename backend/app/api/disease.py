"""
API Endpoints for Chilli Leaf Disease Detection & History
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from backend.app.database.session import get_db
from backend.app.database.models import DiseaseDetection
from backend.app.schemas.disease import DiseasePredictionResponse, DiseaseHistoryItem, DiseaseStatsResponse
from backend.app.services.disease_service import DiseaseService

router = APIRouter(prefix="/api/disease", tags=["Disease Detection"])


@router.post("/predict", response_model=DiseasePredictionResponse)
async def predict_disease(
    file: UploadFile = File(..., description="Chilli leaf image (JPG, PNG, WEBP)"),
    user_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Complete Disease Detection Flow:
    1. Receive image file
    2. Validate format & size
    3. Upload to Cloudinary CDN
    4. Run PyTorch MobileNetV2 Deep Learning Inference
    5. Run Prototype Severity Estimation Layer
    6. Generate Safe Agronomic Guidance
    7. Save to Database
    8. Return complete response
    """
    try:
        file_bytes = await file.read()
        if not file_bytes:
            raise HTTPException(status_code=400, detail="Empty file uploaded.")

        result = DiseaseService.predict_and_store(
            file_bytes=file_bytes,
            filename=file.filename or "leaf.jpg",
            db=db,
            user_id=user_id
        )
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")


@router.get("/history", response_model=List[DiseaseHistoryItem])
def get_disease_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    disease_filter: Optional[str] = Query(None),
    severity_filter: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Fetch disease detection history with Cloudinary image URLs"""
    query = db.query(DiseaseDetection)

    if disease_filter and disease_filter != "all":
        query = query.filter(DiseaseDetection.disease == disease_filter)

    if severity_filter and severity_filter != "all":
        query = query.filter(DiseaseDetection.severity.ilike(f"%{severity_filter}%"))

    records = query.order_by(desc(DiseaseDetection.created_at)).offset(skip).limit(limit).all()
    return records


@router.delete("/history/{record_id}")
def delete_history_record(record_id: int, db: Session = Depends(get_db)):
    """Delete a disease detection record"""
    record = db.query(DiseaseDetection).filter(DiseaseDetection.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found.")

    db.delete(record)
    db.commit()
    return {"message": "Record deleted successfully", "id": record_id}


@router.get("/stats", response_model=DiseaseStatsResponse)
def get_disease_stats(db: Session = Depends(get_db)):
    """Summary metrics for disease detection analytics"""
    total = db.query(DiseaseDetection).count()
    healthy = db.query(DiseaseDetection).filter(DiseaseDetection.disease == "Healthy_Leaf").count()
    diseased = total - healthy

    # Class distribution
    class_counts = db.query(
        DiseaseDetection.disease, func.count(DiseaseDetection.id)
    ).group_by(DiseaseDetection.disease).all()
    disease_dist = {cls_name: count for cls_name, count in class_counts}

    # Severity distribution
    sev_counts = db.query(
        DiseaseDetection.severity, func.count(DiseaseDetection.id)
    ).group_by(DiseaseDetection.severity).all()
    sev_dist = {sev: count for sev, count in sev_counts}

    # Recent scans
    recent = db.query(DiseaseDetection).order_by(desc(DiseaseDetection.created_at)).limit(5).all()

    return {
        "total_scans": total,
        "healthy_count": healthy,
        "diseased_count": diseased,
        "disease_distribution": disease_dist,
        "severity_distribution": sev_dist,
        "recent_detections": recent
    }
