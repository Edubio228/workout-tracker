from app.core.pagination import Pagination
from app.core.pr_checker import check_and_save_prs
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.workout import Workout, WorkoutExercise
from app.models.user import User
from app.schemas.workout import WorkoutCreate, WorkoutUpdate, WorkoutOut
from app.schemas.exercise import ExerciseOut
from app.models.exercise import Exercise
from app.core.security import get_current_user

router = APIRouter(prefix="/workouts", tags=["workouts"])

@router.post(
    "/",
    response_model=WorkoutOut,
    status_code=201,
    summary="Create a new workout",
    response_description="The created workout with all exercises",
)
def create_workout(
    payload: WorkoutCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new workout for the authenticated user.

    Optionally include a list of **exercises** with sets, reps, and weight.
    You can also schedule the workout for a future date using **scheduled_at**.
    """
    workout = Workout(
        user_id=current_user.id,
        title=payload.title,
        notes=payload.notes,
        scheduled_at=payload.scheduled_at,
    )
    db.add(workout)
    db.flush()
    for ex in payload.exercises:
        db.add(WorkoutExercise(workout_id=workout.id, **ex.model_dump()))
    db.commit()
    db.refresh(workout)
    return workout

@router.get("/", response_model=List[WorkoutOut])
def list_workouts(
    status: Optional[str] = None,
    pagination: Pagination = Depends(Pagination),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Workout).filter(Workout.user_id == current_user.id)
    if status:
        q = q.filter(Workout.status == status)
    return q.order_by(Workout.scheduled_at).offset(pagination.skip).limit(pagination.limit).all()

@router.get("/exercises/all", response_model=List[ExerciseOut])
def list_exercises(db: Session = Depends(get_db)):
    return db.query(Exercise).order_by(Exercise.name).all()
    
@router.get(
    "/{workout_id}",
    response_model=WorkoutOut,
    summary="Get a single workout",
    responses={404: {"description": "Workout not found"}},
)
def get_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific workout by ID. Only returns workouts owned by the current user."""
    workout = db.query(Workout).filter(
        Workout.id == workout_id,
        Workout.user_id == current_user.id,
    ).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout

@router.patch(
    "/{workout_id}",
    response_model=WorkoutOut,
    summary="Update a workout",
    responses={404: {"description": "Workout not found"}},
)
def update_workout(
    workout_id: int,
    payload: WorkoutUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update a workout's title, notes, scheduled date, or status.

    Setting **status** to `completed` will automatically check for
    new personal records across all exercises in the workout.
    """
    workout = db.query(Workout).filter(
        Workout.id == workout_id,
        Workout.user_id == current_user.id,
    ).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(workout, field, value)
    db.commit()
    db.refresh(workout)
    if payload.status == "completed":
        check_and_save_prs(current_user.id, workout.id, db)
    return workout

@router.delete(
    "/{workout_id}",
    status_code=204,
    summary="Delete a workout",
    responses={404: {"description": "Workout not found"}},
)
def delete_workout(
    workout_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Permanently delete a workout and all its exercises."""
    workout = db.query(Workout).filter(
        Workout.id == workout_id,
        Workout.user_id == current_user.id,
    ).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    db.delete(workout)
    db.commit()