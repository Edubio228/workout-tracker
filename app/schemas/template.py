from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TemplateExerciseCreate(BaseModel):
    exercise_id:   int
    sets:          Optional[int]   = None
    reps:          Optional[int]   = None
    weight_kg:     Optional[float] = None
    duration_secs: Optional[int]   = None
    notes:         Optional[str]   = None

class TemplateExerciseOut(TemplateExerciseCreate):
    id: int
    model_config = {"from_attributes": True}

class TemplateCreate(BaseModel):
    title:     str
    notes:     Optional[str] = None
    exercises: List[TemplateExerciseCreate] = []

class TemplateUpdate(BaseModel):
    title: Optional[str] = None
    notes: Optional[str] = None

class TemplateOut(BaseModel):
    id:         int
    title:      str
    notes:      Optional[str]
    created_at: datetime
    exercises:  List[TemplateExerciseOut] = []
    model_config = {"from_attributes": True}

class SpawnWorkoutRequest(BaseModel):
    scheduled_at: Optional[datetime] = None