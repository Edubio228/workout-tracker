from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Optional
from collections import defaultdict
from app.db.session import get_db
from app.models.workout import Workout, WorkoutExercise
from app.models.exercise import Exercise
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get(
    "/exercise/{exercise_id}",
    summary="Strength curve for one exercise",
    response_description="Best weight per completed session, oldest first",
)
def exercise_progress(
    exercise_id: int,
    days: int = 90,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns the best weight lifted for a given exercise across all
    completed workouts in the last N **days** (default 90).

    Each entry represents one workout session. Use this data to plot
    a strength curve over time.
    """
    since = datetime.utcnow() - timedelta(days=days)

    rows = (
        db.query(
            Workout.scheduled_at,
            Workout.title,
            func.max(WorkoutExercise.weight_kg).label("best_weight"),
            func.max(WorkoutExercise.reps).label("best_reps"),
            func.sum(
                WorkoutExercise.sets * WorkoutExercise.reps * WorkoutExercise.weight_kg
            ).label("session_volume"),
        )
        .join(WorkoutExercise, WorkoutExercise.workout_id == Workout.id)
        .filter(
            Workout.user_id == current_user.id,
            Workout.status == "completed",
            Workout.scheduled_at >= since,
            WorkoutExercise.exercise_id == exercise_id,
        )
        .group_by(Workout.id)
        .order_by(Workout.scheduled_at)
        .all()
    )

    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()

    return {
        "exercise_id": exercise_id,
        "exercise_name": exercise.name if exercise else "Unknown",
        "period_days": days,
        "data": [
            {
                "date": row.scheduled_at,
                "workout_title": row.title,
                "best_weight_kg": round(row.best_weight or 0, 2),
                "best_reps": row.best_reps or 0,
                "session_volume_kg": round(row.session_volume or 0, 2),
            }
            for row in rows
        ],
    }


@router.get(
    "/volume",
    summary="Total volume lifted per week",
    response_description="Weekly volume in kg over the last N days",
)
def volume_over_time(
    days: int = 90,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns total volume (sets × reps × weight) grouped by week
    over the last N **days** (default 90).

    Use this to plot overall training effort over time.
    """
    since = datetime.utcnow() - timedelta(days=days)

    rows = (
        db.query(
            Workout.scheduled_at,
            WorkoutExercise.sets,
            WorkoutExercise.reps,
            WorkoutExercise.weight_kg,
        )
        .join(WorkoutExercise, WorkoutExercise.workout_id == Workout.id)
        .filter(
            Workout.user_id == current_user.id,
            Workout.status == "completed",
            Workout.scheduled_at >= since,
        )
        .all()
    )

    # Group by week
    weekly = defaultdict(float)
    for row in rows:
        if row.scheduled_at:
            # Get the Monday of the week this workout falls in
            week_start = row.scheduled_at - timedelta(days=row.scheduled_at.weekday())
            week_key = week_start.strftime("%Y-%m-%d")
            volume = (row.sets or 0) * (row.reps or 0) * (row.weight_kg or 0)
            weekly[week_key] += volume

    return {
        "period_days": days,
        "unit": "kg",
        "data": [
            {"week_starting": week, "volume_kg": round(vol, 2)}
            for week, vol in sorted(weekly.items())
        ],
    }


@router.get(
    "/workouts",
    summary="Workout frequency per week",
    response_description="Number of completed workouts per week",
)
def workout_frequency(
    days: int = 90,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns the number of completed workouts per week over the
    last N **days** (default 90).

    Use this to track consistency — how often you actually showed up.
    """
    since = datetime.utcnow() - timedelta(days=days)

    workouts = (
        db.query(Workout)
        .filter(
            Workout.user_id == current_user.id,
            Workout.status == "completed",
            Workout.scheduled_at >= since,
        )
        .all()
    )

    weekly = defaultdict(int)
    for w in workouts:
        if w.scheduled_at:
            week_start = w.scheduled_at - timedelta(days=w.scheduled_at.weekday())
            week_key = week_start.strftime("%Y-%m-%d")
            weekly[week_key] += 1

    return {
        "period_days": days,
        "data": [
            {"week_starting": week, "workouts_completed": count}
            for week, count in sorted(weekly.items())
        ],
    }