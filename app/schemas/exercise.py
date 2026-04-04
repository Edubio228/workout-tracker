from pydantic import BaseModel
from typing import Optional

class ExerciseCreate(BaseModel):
    name:         str
    description:  Optional[str] = None
    category:     Optional[str] = None
    muscle_group: Optional[str] = None

class ExerciseUpdate(BaseModel):
    name:         Optional[str] = None
    description:  Optional[str] = None
    category:     Optional[str] = None
    muscle_group: Optional[str] = None

class ExerciseOut(BaseModel):
    id:           int
    name:         str
    description:  Optional[str]
    category:     Optional[str]
    muscle_group: Optional[str]
    user_id:      Optional[int]  # None = global, int = custom
    model_config  = {"from_attributes": True}