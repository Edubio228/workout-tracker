from pydantic import BaseModel
from datetime import datetime

class PersonalRecordOut(BaseModel):
    id:          int
    exercise_id: int
    record_type: str
    value:       float
    achieved_at: datetime
    model_config = {"from_attributes": True}