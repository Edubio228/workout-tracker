from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.workout import WorkoutExercise, PersonalRecord, Workout

def check_and_save_prs(user_id: int, workout_id: int, db: Session) -> list[PersonalRecord]:
    """
    After a workout is marked completed, check every exercise in it
    for new personal records. Saves any new PRs and returns them.
    """
    new_prs = []

    exercises = (
        db.query(WorkoutExercise)
        .join(Workout)
        .filter(
            Workout.id == workout_id,
            Workout.user_id == user_id,
        )
        .all()
    )

    for we in exercises:
        candidates = {
            "max_weight": we.weight_kg or 0,
            "max_reps":   we.reps or 0,
            "max_volume": (we.sets or 0) * (we.reps or 0) * (we.weight_kg or 0),
        }

        for record_type, new_value in candidates.items():
            if new_value <= 0:
                continue

            # Find the current PR for this user + exercise + type
            current_pr = (
                db.query(PersonalRecord)
                .filter(
                    PersonalRecord.user_id     == user_id,
                    PersonalRecord.exercise_id == we.exercise_id,
                    PersonalRecord.record_type == record_type,
                )
                .first()
            )

            if current_pr is None:
                # First time logging this exercise — it's automatically a PR
                pr = PersonalRecord(
                    user_id=user_id,
                    exercise_id=we.exercise_id,
                    record_type=record_type,
                    value=new_value,
                )
                db.add(pr)
                new_prs.append(pr)

            elif new_value > current_pr.value:
                # Beat the old record — update it
                current_pr.value = new_value
                current_pr.achieved_at = func.now()
                new_prs.append(current_pr)

    db.commit()
    return new_prs