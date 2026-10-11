"""
Pydantic Schemas for Disease Detection
"""
from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field


class DiseasePredictionResponse(BaseModel):
    id: Optional[int] = None
    crop: str = "Chilli (Capsicum annuum)"
    disease: str
    disease_display_name: str
    scientific_name: str
    confidence: float
    severity: str
    severity_level: int
    lesion_coverage_percent: float
    severity_method: str
    recommendation: str
    description: Dict[str, str]
    recommendations_list: Dict[str, List[str]]
    all_probabilities: Dict[str, float]
    image_url: str
    cloudinary_public_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class DiseaseHistoryItem(BaseModel):
    id: int
    user_id: Optional[int] = None
    crop: str
    image_url: str
    cloudinary_public_id: Optional[str] = None
    disease: str
    confidence: float
    severity: str
    severity_level: Optional[int] = 1
    lesion_coverage_percent: Optional[float] = 0.0
    recommendation: str
    created_at: datetime

    class Config:
        from_attributes = True


class DiseaseStatsResponse(BaseModel):
    total_scans: int
    healthy_count: int
    diseased_count: int
    disease_distribution: Dict[str, int]
    severity_distribution: Dict[str, int]
    recent_detections: List[DiseaseHistoryItem]
