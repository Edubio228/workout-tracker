from app.core.pagination import Pagination
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.workout import WorkoutTemplate, TemplateExercise, Workout, WorkoutExercise
from app.models.user import User
from app.schemas.template import TemplateCreate, TemplateUpdate, TemplateOut, SpawnWorkoutRequest
from app.schemas.workout import WorkoutOut
from app.core.security import get_current_user

router = APIRouter(prefix="/templates", tags=["templates"])

@router.post(
    "/",
    response_model=TemplateOut,
    status_code=201,
    summary="Create a workout template",
    response_description="The created template with exercises",
)
def create_template(
    payload: TemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a reusable workout template.

    Templates store a workout structure — title, notes, and a list of
    exercises with default sets, reps, and weights. Use the **spawn**
    endpoint to create a real workout from a template.
    """
    template = WorkoutTemplate(
        user_id=current_user.id,
        title=payload.title,
        notes=payload.notes,
    )
    db.add(template)
    db.flush()
    for ex in payload.exercises:
        db.add(TemplateExercise(template_id=template.id, **ex.model_dump()))
    db.commit()
    db.refresh(template)
    return template

@router.get("/", response_model=List[TemplateOut])
def list_templates(
    pagination:   Pagination = Depends(Pagination),
    db:           Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(WorkoutTemplate)
        .filter(WorkoutTemplate.user_id == current_user.id)
        .order_by(WorkoutTemplate.created_at.desc())
        .offset(pagination.skip)
        .limit(pagination.limit)
        .all()
    )

@router.get(
    "/{template_id}",
    response_model=TemplateOut,
    summary="Get a single template",
    responses={404: {"description": "Template not found"}},
)
def get_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific template by ID."""
    template = db.query(WorkoutTemplate).filter(
        WorkoutTemplate.id == template_id,
        WorkoutTemplate.user_id == current_user.id,
    ).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.patch(
    "/{template_id}",
    response_model=TemplateOut,
    summary="Update a template",
    responses={404: {"description": "Template not found"}},
)
def update_template(
    template_id: int,
    payload: TemplateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a template's title or notes."""
    template = db.query(WorkoutTemplate).filter(
        WorkoutTemplate.id == template_id,
        WorkoutTemplate.user_id == current_user.id,
    ).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(template, field, value)
    db.commit()
    db.refresh(template)
    return template

@router.delete(
    "/{template_id}",
    status_code=204,
    summary="Delete a template",
    responses={404: {"description": "Template not found"}},
)
def delete_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a template. This does not affect any workouts spawned from it."""
    template = db.query(WorkoutTemplate).filter(
        WorkoutTemplate.id == template_id,
        WorkoutTemplate.user_id == current_user.id,
    ).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    db.delete(template)
    db.commit()

@router.post(
    "/{template_id}/spawn",
    response_model=WorkoutOut,
    status_code=201,
    summary="Spawn a workout from a template",
    response_description="A new workout pre-filled with the template's exercises",
    responses={404: {"description": "Template not found"}},
)
def spawn_workout(
    template_id: int,
    payload: SpawnWorkoutRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new workout pre-filled from a template.

    The template is not modified — a completely independent workout
    is created with all the same exercises, sets, reps, and weights.
    Optionally provide **scheduled_at** to set the workout date.
    """
    template = db.query(WorkoutTemplate).filter(
        WorkoutTemplate.id == template_id,
        WorkoutTemplate.user_id == current_user.id,
    ).first()
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    workout = Workout(
        user_id=current_user.id,
        title=template.title,
        notes=template.notes,
        scheduled_at=payload.scheduled_at,
        status="pending",
    )
    db.add(workout)
    db.flush()
    for tex in template.exercises:
        db.add(WorkoutExercise(
            workout_id=workout.id,
            exercise_id=tex.exercise_id,
            sets=tex.sets,
            reps=tex.reps,
            weight_kg=tex.weight_kg,
            duration_secs=tex.duration_secs,
            notes=tex.notes,
        ))
    db.commit()
    db.refresh(workout)
    return workout