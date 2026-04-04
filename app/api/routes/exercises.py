from app.core.pagination import Pagination
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.exercise import Exercise
from app.models.user import User
from app.schemas.exercise import ExerciseCreate, ExerciseUpdate, ExerciseOut
from app.core.security import get_current_user

router = APIRouter(prefix="/exercises", tags=["exercises"])

@router.get("/", response_model=List[ExerciseOut])
def list_exercises(
    category:     Optional[str] = None,
    muscle_group: Optional[str] = None,
    pagination:   Pagination = Depends(Pagination),
    db:           Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Exercise).filter(
        (Exercise.user_id == None) | (Exercise.user_id == current_user.id)
    )
    if category:
        query = query.filter(Exercise.category == category)
    if muscle_group:
        query = query.filter(Exercise.muscle_group == muscle_group)
    return query.order_by(Exercise.name).offset(pagination.skip).limit(pagination.limit).all()

@router.post(
    "/",
    response_model=ExerciseOut,
    status_code=201,
    summary="Create a custom exercise",
    response_description="The newly created custom exercise",
)
def create_exercise(
    payload: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a custom exercise owned by the current user.

    Custom exercises appear in your exercise list alongside
    the global library and can be used in workouts and templates.
    """
    existing = db.query(Exercise).filter(
        Exercise.name == payload.name,
        (Exercise.user_id == None) | (Exercise.user_id == current_user.id)
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="An exercise with this name already exists"
        )
    exercise = Exercise(
        name=payload.name,
        description=payload.description,
        category=payload.category,
        muscle_group=payload.muscle_group,
        user_id=current_user.id,
    )
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise

@router.patch(
    "/{exercise_id}",
    response_model=ExerciseOut,
    summary="Update a custom exercise",
    responses={
        404: {"description": "Exercise not found"},
        403: {"description": "Cannot edit a global exercise"},
    },
)
def update_exercise(
    exercise_id: int,
    payload: ExerciseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a custom exercise. You can only edit exercises you created —
    global seeded exercises cannot be modified.
    """
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    if exercise.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only edit your own custom exercises"
        )
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(exercise, field, value)
    db.commit()
    db.refresh(exercise)
    return exercise

@router.delete(
    "/{exercise_id}",
    status_code=204,
    summary="Delete a custom exercise",
    responses={
        404: {"description": "Exercise not found"},
        403: {"description": "Cannot delete a global exercise"},
    },
)
def delete_exercise(
    exercise_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a custom exercise. You can only delete exercises you created —
    global seeded exercises cannot be deleted.
    """
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    if exercise.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own custom exercises"
        )
    db.delete(exercise)
    db.commit()