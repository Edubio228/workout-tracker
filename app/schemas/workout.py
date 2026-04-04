from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class WorkoutExerciseCreate(BaseModel):
    exercise_id:   int
    sets:          Optional[int]   = None
    reps:          Optional[int]   = None
    weight_kg:     Optional[float] = None
    duration_secs: Optional[int]   = None
    notes:         Optional[str]   = None

class WorkoutExerciseOut(WorkoutExerciseCreate):
    id: int
    model_config = {"from_attributes": True}

class WorkoutCreate(BaseModel):
    title:        str
    notes:        Optional[str]      = None
    scheduled_at: Optional[datetime] = None
    exercises:    List[WorkoutExerciseCreate] = []

class WorkoutUpdate(BaseModel):
    title:        Optional[str]      = None
    notes:        Optional[str]      = None
    scheduled_at: Optional[datetime] = None
    status:       Optional[str]      = None

class WorkoutOut(BaseModel):
    id:           int
    title:        str
    notes:        Optional[str]
    scheduled_at: Optional[datetime]
    status:       str
    created_at:   datetime
    exercises:    List[WorkoutExerciseOut] = []
    model_config = {"from_attributes": True}