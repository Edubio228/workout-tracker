from app.core.pagination import Pagination
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.workout import PersonalRecord
from app.models.user import User
from app.schemas.personal_record import PersonalRecordOut
from app.core.security import get_current_user

router = APIRouter(prefix="/personal-records", tags=["personal records"])

@router.get("/", response_model=List[PersonalRecordOut])
def get_all_prs(
    pagination:   Pagination = Depends(Pagination),
    db:           Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(PersonalRecord)
        .filter(PersonalRecord.user_id == current_user.id)
        .order_by(PersonalRecord.achieved_at.desc())
        .offset(pagination.skip)
        .limit(pagination.limit)
        .all()
    )

@router.get(
    "/exercise/{exercise_id}",
    response_model=List[PersonalRecordOut],
    summary="Get PRs for a specific exercise",
    responses={404: {"description": "No records found for this exercise"}},
)
def get_prs_for_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all personal record types for one specific exercise."""
    return (
        db.query(PersonalRecord)
        .filter(
            PersonalRecord.user_id == current_user.id,
            PersonalRecord.exercise_id == exercise_id,
        )
        .all()
    )