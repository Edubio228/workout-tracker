from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.db.session import get_db
from app.models.workout import Workout
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get(
    "/summary",
    summary="Get workout summary",
    response_description="Aggregated stats for the requested time period",
)
def summary(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns a summary of workouts over the last N **days** (default 30).

    Includes total workouts, completed, skipped, pending,
    and total volume lifted in kg (sets × reps × weight).
    """
    since = datetime.utcnow() - timedelta(days=days)
    workouts = (
        db.query(Workout)
        .filter(Workout.user_id == current_user.id, Workout.scheduled_at >= since)
        .all()
    )
    completed = [w for w in workouts if w.status == "completed"]
    total_volume = sum(
        (we.sets or 0) * (we.reps or 0) * (we.weight_kg or 0)
        for w in completed
        for we in w.exercises
    )
    return {
        "period_days": days,
        "total_workouts": len(workouts),
        "completed": len(completed),
        "skipped": len([w for w in workouts if w.status == "skipped"]),
        "pending": len([w for w in workouts if w.status == "pending"]),
        "total_volume_kg": round(total_volume, 2),
    }