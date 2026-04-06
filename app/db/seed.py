from app.models.exercise import Exercise

EXERCISES = [
    # ── Chest ──────────────────────────────────────────────────────────
    {"name": "Bench Press",           "category": "strength",    "muscle_group": "chest",     "description": "Barbell press on a flat bench"},
    {"name": "Incline Bench Press",   "category": "strength",    "muscle_group": "chest",     "description": "Barbell press on an incline bench"},
    {"name": "Decline Bench Press",   "category": "strength",    "muscle_group": "chest",     "description": "Barbell press on a decline bench"},
    {"name": "Dumbbell Chest Fly",    "category": "strength",    "muscle_group": "chest",     "description": "Dumbbell fly on a flat bench"},
    {"name": "Incline Dumbbell Fly",  "category": "strength",    "muscle_group": "chest",     "description": "Dumbbell fly on an incline bench"},
    {"name": "Cable Fly",             "category": "strength",    "muscle_group": "chest",     "description": "Cable crossover fly"},
    {"name": "Push-up",               "category": "strength",    "muscle_group": "chest",     "description": "Bodyweight push-up"},
    {"name": "Dips",                  "category": "strength",    "muscle_group": "chest",     "description": "Parallel bar dips for chest"},
    {"name": "Chest Press Machine",   "category": "strength",    "muscle_group": "chest",     "description": "Machine chest press"},
    {"name": "Pec Deck",              "category": "strength",    "muscle_group": "chest",     "description": "Machine pec deck fly"},

    # ── Back ───────────────────────────────────────────────────────────
    {"name": "Deadlift",              "category": "strength",    "muscle_group": "back",      "description": "Conventional barbell deadlift"},
    {"name": "Pull-up",               "category": "strength",    "muscle_group": "back",      "description": "Bodyweight pull-up to bar"},
    {"name": "Chin-up",               "category": "strength",    "muscle_group": "back",      "description": "Underhand grip pull-up"},
    {"name": "Barbell Row",           "category": "strength",    "muscle_group": "back",      "description": "Bent-over barbell row"},
    {"name": "Dumbbell Row",          "category": "strength",    "muscle_group": "back",      "description": "Single arm dumbbell row"},
    {"name": "Cable Row",             "category": "strength",    "muscle_group": "back",      "description": "Seated cable row"},
    {"name": "Lat Pulldown",          "category": "strength",    "muscle_group": "back",      "description": "Cable lat pulldown"},
    {"name": "T-Bar Row",             "category": "strength",    "muscle_group": "back",      "description": "T-bar or landmine row"},
    {"name": "Face Pull",             "category": "strength",    "muscle_group": "back",      "description": "Cable face pull for rear delts and upper back"},
    {"name": "Good Morning",          "category": "strength",    "muscle_group": "back",      "description": "Barbell good morning for lower back"},

    # ── Shoulders ──────────────────────────────────────────────────────
    {"name": "Overhead Press",        "category": "strength",    "muscle_group": "shoulders", "description": "Standing barbell overhead press"},
    {"name": "Seated Dumbbell Press", "category": "strength",    "muscle_group": "shoulders", "description": "Seated dumbbell shoulder press"},
    {"name": "Arnold Press",          "category": "strength",    "muscle_group": "shoulders", "description": "Rotating dumbbell shoulder press"},
    {"name": "Lateral Raise",         "category": "strength",    "muscle_group": "shoulders", "description": "Dumbbell lateral raise"},
    {"name": "Front Raise",           "category": "strength",    "muscle_group": "shoulders", "description": "Dumbbell front raise"},
    {"name": "Rear Delt Fly",         "category": "strength",    "muscle_group": "shoulders", "description": "Dumbbell rear delt fly"},
    {"name": "Upright Row",           "category": "strength",    "muscle_group": "shoulders", "description": "Barbell or dumbbell upright row"},
    {"name": "Shrugs",                "category": "strength",    "muscle_group": "shoulders", "description": "Barbell or dumbbell shrugs for traps"},

    # ── Arms ───────────────────────────────────────────────────────────
    {"name": "Barbell Curl",          "category": "strength",    "muscle_group": "arms",      "description": "Standing barbell bicep curl"},
    {"name": "Dumbbell Curl",         "category": "strength",    "muscle_group": "arms",      "description": "Alternating dumbbell bicep curl"},
    {"name": "Hammer Curl",           "category": "strength",    "muscle_group": "arms",      "description": "Neutral grip dumbbell curl"},
    {"name": "Preacher Curl",         "category": "strength",    "muscle_group": "arms",      "description": "Barbell curl on preacher bench"},
    {"name": "Cable Curl",            "category": "strength",    "muscle_group": "arms",      "description": "Standing cable bicep curl"},
    {"name": "Tricep Pushdown",       "category": "strength",    "muscle_group": "arms",      "description": "Cable tricep pushdown"},
    {"name": "Skull Crushers",        "category": "strength",    "muscle_group": "arms",      "description": "Lying barbell or EZ-bar tricep extension"},
    {"name": "Overhead Tricep Extension", "category": "strength","muscle_group": "arms",      "description": "Dumbbell overhead tricep extension"},
    {"name": "Close Grip Bench Press","category": "strength",    "muscle_group": "arms",      "description": "Close grip barbell bench for triceps"},
    {"name": "Diamond Push-up",       "category": "strength",    "muscle_group": "arms",      "description": "Close grip push-up for triceps"},

    # ── Legs ───────────────────────────────────────────────────────────
    {"name": "Squat",                 "category": "strength",    "muscle_group": "legs",      "description": "Barbell back squat"},
    {"name": "Front Squat",           "category": "strength",    "muscle_group": "legs",      "description": "Barbell front squat"},
    {"name": "Leg Press",             "category": "strength",    "muscle_group": "legs",      "description": "Machine leg press"},
    {"name": "Romanian Deadlift",     "category": "strength",    "muscle_group": "legs",      "description": "Barbell Romanian deadlift for hamstrings"},
    {"name": "Lunges",                "category": "strength",    "muscle_group": "legs",      "description": "Barbell or dumbbell lunges"},
    {"name": "Bulgarian Split Squat", "category": "strength",    "muscle_group": "legs",      "description": "Rear foot elevated split squat"},
    {"name": "Leg Curl",              "category": "strength",    "muscle_group": "legs",      "description": "Machine lying or seated leg curl"},
    {"name": "Leg Extension",         "category": "strength",    "muscle_group": "legs",      "description": "Machine leg extension for quads"},
    {"name": "Calf Raise",            "category": "strength",    "muscle_group": "legs",      "description": "Standing or seated calf raise"},
    {"name": "Hack Squat",            "category": "strength",    "muscle_group": "legs",      "description": "Machine hack squat"},
    {"name": "Step-up",               "category": "strength",    "muscle_group": "legs",      "description": "Dumbbell step-up onto bench"},
    {"name": "Hip Thrust",            "category": "strength",    "muscle_group": "legs",      "description": "Barbell hip thrust for glutes"},
    {"name": "Glute Bridge",          "category": "strength",    "muscle_group": "legs",      "description": "Bodyweight or loaded glute bridge"},
    {"name": "Sumo Deadlift",         "category": "strength",    "muscle_group": "legs",      "description": "Wide stance sumo deadlift"},

    # ── Core ───────────────────────────────────────────────────────────
    {"name": "Plank",                 "category": "flexibility", "muscle_group": "core",      "description": "Static core hold"},
    {"name": "Crunch",                "category": "strength",    "muscle_group": "core",      "description": "Basic abdominal crunch"},
    {"name": "Sit-up",                "category": "strength",    "muscle_group": "core",      "description": "Full range sit-up"},
    {"name": "Leg Raise",             "category": "strength",    "muscle_group": "core",      "description": "Hanging or lying leg raise"},
    {"name": "Russian Twist",         "category": "strength",    "muscle_group": "core",      "description": "Weighted or bodyweight Russian twist"},
    {"name": "Ab Wheel Rollout",      "category": "strength",    "muscle_group": "core",      "description": "Ab wheel rollout from knees or standing"},
    {"name": "Cable Crunch",          "category": "strength",    "muscle_group": "core",      "description": "Kneeling cable crunch"},
    {"name": "Mountain Climber",      "category": "cardio",      "muscle_group": "core",      "description": "Dynamic mountain climber"},
    {"name": "Side Plank",            "category": "flexibility", "muscle_group": "core",      "description": "Lateral static core hold"},

    # ── Cardio ─────────────────────────────────────────────────────────
    {"name": "Running",               "category": "cardio",      "muscle_group": "full body", "description": "Outdoor or treadmill running"},
    {"name": "Cycling",               "category": "cardio",      "muscle_group": "legs",      "description": "Bike or stationary cycle"},
    {"name": "Jump Rope",             "category": "cardio",      "muscle_group": "full body", "description": "Skipping rope"},
    {"name": "Rowing Machine",        "category": "cardio",      "muscle_group": "full body", "description": "Cardio rowing machine"},
    {"name": "Elliptical",            "category": "cardio",      "muscle_group": "full body", "description": "Elliptical cross trainer"},
    {"name": "Stair Climber",         "category": "cardio",      "muscle_group": "legs",      "description": "Stair climber machine"},
    {"name": "Burpees",               "category": "cardio",      "muscle_group": "full body", "description": "Full body burpee"},
    {"name": "Jumping Jacks",         "category": "cardio",      "muscle_group": "full body", "description": "Classic jumping jacks"},
    {"name": "Box Jump",              "category": "cardio",      "muscle_group": "legs",      "description": "Explosive jump onto a box"},
    {"name": "Battle Ropes",          "category": "cardio",      "muscle_group": "full body", "description": "Heavy rope wave exercises"},
    {"name": "Swimming",              "category": "cardio",      "muscle_group": "full body", "description": "Pool or open water swimming"},
    {"name": "Sprint Intervals",      "category": "cardio",      "muscle_group": "full body", "description": "High intensity sprint intervals"},

    # ── Flexibility ────────────────────────────────────────────────────
    {"name": "Hip Flexor Stretch",    "category": "flexibility", "muscle_group": "hips",      "description": "Kneeling hip flexor stretch"},
    {"name": "Hamstring Stretch",     "category": "flexibility", "muscle_group": "legs",      "description": "Standing or seated hamstring stretch"},
    {"name": "Quad Stretch",          "category": "flexibility", "muscle_group": "legs",      "description": "Standing quad stretch"},
    {"name": "Chest Stretch",         "category": "flexibility", "muscle_group": "chest",     "description": "Doorway or band chest stretch"},
    {"name": "Child's Pose",          "category": "flexibility", "muscle_group": "back",      "description": "Yoga child's pose for back and hips"},
    {"name": "Cat-Cow Stretch",       "category": "flexibility", "muscle_group": "back",      "description": "Spinal mobility stretch"},
    {"name": "Pigeon Pose",           "category": "flexibility", "muscle_group": "hips",      "description": "Deep hip opener stretch"},
    {"name": "Shoulder Cross Stretch","category": "flexibility", "muscle_group": "shoulders", "description": "Cross-body shoulder stretch"},
    {"name": "Tricep Stretch",        "category": "flexibility", "muscle_group": "arms",      "description": "Overhead tricep and shoulder stretch"},
    {"name": "Calf Stretch",          "category": "flexibility", "muscle_group": "legs",      "description": "Wall calf stretch"},
]

def seed_exercises(db=None):
    close_after = False
    if db is None:
        from app.db.session import SessionLocal
        db = SessionLocal()
        close_after = True
    try:
        added = 0
        for data in EXERCISES:
            if not db.query(Exercise).filter_by(name=data["name"]).first():
                db.add(Exercise(**data))
                added += 1
        db.commit()
        print(f"Seeded {added} new exercises ({len(EXERCISES)} total).")
    finally:
        if close_after:
            db.close()