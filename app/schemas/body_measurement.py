from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BodyMeasurementCreate(BaseModel):
    logged_at:    Optional[datetime] = None
    weight_kg:    Optional[float]    = None
    body_fat_pct: Optional[float]    = None
    chest_cm:     Optional[float]    = None
    waist_cm:     Optional[float]    = None
    hips_cm:      Optional[float]    = None
    arms_cm:      Optional[float]    = None
    legs_cm:      Optional[float]    = None
    notes:        Optional[str]      = None

class BodyMeasurementUpdate(BodyMeasurementCreate):
    pass

class BodyMeasurementOut(BaseModel):
    id:           int
    logged_at:    datetime
    weight_kg:    Optional[float]
    body_fat_pct: Optional[float]
    chest_cm:     Optional[float]
    waist_cm:     Optional[float]
    hips_cm:      Optional[float]
    arms_cm:      Optional[float]
    legs_cm:      Optional[float]
    notes:        Optional[str]
    model_config  = {"from_attributes": True}