from app.models.exercise import Exercise

EXERCISES = [
    {"name": "Bench Press",       "category": "strength",    "muscle_group": "chest",     "description": "Barbell press on a flat bench"},
    {"name": "Squat",             "category": "strength",    "muscle_group": "legs",      "description": "Barbell back squat"},
    {"name": "Deadlift",          "category": "strength",    "muscle_group": "back",      "description": "Conventional barbell deadlift"},
    {"name": "Pull-up",           "category": "strength",    "muscle_group": "back",      "description": "Bodyweight pull-up to bar"},
    {"name": "Overhead Press",    "category": "strength",    "muscle_group": "shoulders", "description": "Standing barbell press"},
    {"name": "Barbell Row",       "category": "strength",    "muscle_group": "back",      "description": "Bent-over barbell row"},
    {"name": "Running",           "category": "cardio",      "muscle_group": "full body", "description": "Outdoor or treadmill running"},
    {"name": "Cycling",           "category": "cardio",      "muscle_group": "legs",      "description": "Bike or stationary cycle"},
    {"name": "Plank",             "category": "flexibility", "muscle_group": "core",      "description": "Static core hold"},
    {"name": "Hip Flexor Stretch","category": "flexibility", "muscle_group": "hips",      "description": "Kneeling hip flexor stretch"},
]

def seed_exercises(db=None):
    """Seed exercises. If db session provided, uses it. Otherwise creates its own."""
    close_after = False
    if db is None:
        from app.db.session import SessionLocal
        db = SessionLocal()
        close_after = True
    try:
        for data in EXERCISES:
            if not db.query(Exercise).filter_by(name=data["name"]).first():
                db.add(Exercise(**data))
        db.commit()
        print(f"Seeded {len(EXERCISES)} exercises.")
    finally:
        if close_after:
            db.close()