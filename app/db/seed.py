from app.models.exercise import Exercise

EXERCISES = [
    # ── Chest ──────────────────────────────────────────────────────────
    {"name": "Bench Press",           "category": "strength",    "muscle_group": "chest",     "description": "Barbell press on a flat bench",                   "gif_url": "https://v2.exercisedb.io/image/gifs/0006.gif"},
    {"name": "Incline Bench Press",   "category": "strength",    "muscle_group": "chest",     "description": "Barbell press on an incline bench",               "gif_url": "https://v2.exercisedb.io/image/gifs/0007.gif"},
    {"name": "Decline Bench Press",   "category": "strength",    "muscle_group": "chest",     "description": "Barbell press on a decline bench",                "gif_url": "https://v2.exercisedb.io/image/gifs/1462.gif"},
    {"name": "Dumbbell Chest Fly",    "category": "strength",    "muscle_group": "chest",     "description": "Dumbbell fly on a flat bench",                    "gif_url": "https://v2.exercisedb.io/image/gifs/0327.gif"},
    {"name": "Incline Dumbbell Fly",  "category": "strength",    "muscle_group": "chest",     "description": "Dumbbell fly on an incline bench",                "gif_url": "https://v2.exercisedb.io/image/gifs/0332.gif"},
    {"name": "Cable Fly",             "category": "strength",    "muscle_group": "chest",     "description": "Cable crossover fly",                            "gif_url": "https://v2.exercisedb.io/image/gifs/0259.gif"},
    {"name": "Push-up",               "category": "strength",    "muscle_group": "chest",     "description": "Bodyweight push-up",                             "gif_url": "https://v2.exercisedb.io/image/gifs/0557.gif"},
    {"name": "Dips",                  "category": "strength",    "muscle_group": "chest",     "description": "Parallel bar dips for chest",                    "gif_url": "https://v2.exercisedb.io/image/gifs/0309.gif"},
    {"name": "Chest Press Machine",   "category": "strength",    "muscle_group": "chest",     "description": "Machine chest press",                            "gif_url": "https://v2.exercisedb.io/image/gifs/0289.gif"},
    {"name": "Pec Deck",              "category": "strength",    "muscle_group": "chest",     "description": "Machine pec deck fly",                           "gif_url": "https://v2.exercisedb.io/image/gifs/0484.gif"},

    # ── Back ───────────────────────────────────────────────────────────
    {"name": "Deadlift",              "category": "strength",    "muscle_group": "back",      "description": "Conventional barbell deadlift",                  "gif_url": "https://v2.exercisedb.io/image/gifs/0032.gif"},
    {"name": "Pull-up",               "category": "strength",    "muscle_group": "back",      "description": "Bodyweight pull-up to bar",                      "gif_url": "https://v2.exercisedb.io/image/gifs/0543.gif"},
    {"name": "Chin-up",               "category": "strength",    "muscle_group": "back",      "description": "Underhand grip pull-up",                         "gif_url": "https://v2.exercisedb.io/image/gifs/0292.gif"},
    {"name": "Barbell Row",           "category": "strength",    "muscle_group": "back",      "description": "Bent-over barbell row",                          "gif_url": "https://v2.exercisedb.io/image/gifs/0034.gif"},
    {"name": "Dumbbell Row",          "category": "strength",    "muscle_group": "back",      "description": "Single arm dumbbell row",                        "gif_url": "https://v2.exercisedb.io/image/gifs/0355.gif"},
    {"name": "Cable Row",             "category": "strength",    "muscle_group": "back",      "description": "Seated cable row",                               "gif_url": "https://v2.exercisedb.io/image/gifs/0270.gif"},
    {"name": "Lat Pulldown",          "category": "strength",    "muscle_group": "back",      "description": "Cable lat pulldown",                             "gif_url": "https://v2.exercisedb.io/image/gifs/0018.gif"},
    {"name": "T-Bar Row",             "category": "strength",    "muscle_group": "back",      "description": "T-bar or landmine row",                          "gif_url": "https://v2.exercisedb.io/image/gifs/0653.gif"},
    {"name": "Face Pull",             "category": "strength",    "muscle_group": "back",      "description": "Cable face pull for rear delts and upper back",  "gif_url": "https://v2.exercisedb.io/image/gifs/0368.gif"},
    {"name": "Good Morning",          "category": "strength",    "muscle_group": "back",      "description": "Barbell good morning for lower back",            "gif_url": "https://v2.exercisedb.io/image/gifs/0393.gif"},

    # ── Shoulders ──────────────────────────────────────────────────────
    {"name": "Overhead Press",        "category": "strength",    "muscle_group": "shoulders", "description": "Standing barbell overhead press",                "gif_url": "https://v2.exercisedb.io/image/gifs/0066.gif"},
    {"name": "Seated Dumbbell Press", "category": "strength",    "muscle_group": "shoulders", "description": "Seated dumbbell shoulder press",                 "gif_url": "https://v2.exercisedb.io/image/gifs/0345.gif"},
    {"name": "Arnold Press",          "category": "strength",    "muscle_group": "shoulders", "description": "Rotating dumbbell shoulder press",               "gif_url": "https://v2.exercisedb.io/image/gifs/0318.gif"},
    {"name": "Lateral Raise",         "category": "strength",    "muscle_group": "shoulders", "description": "Dumbbell lateral raise",                        "gif_url": "https://v2.exercisedb.io/image/gifs/0342.gif"},
    {"name": "Front Raise",           "category": "strength",    "muscle_group": "shoulders", "description": "Dumbbell front raise",                          "gif_url": "https://v2.exercisedb.io/image/gifs/0373.gif"},
    {"name": "Rear Delt Fly",         "category": "strength",    "muscle_group": "shoulders", "description": "Dumbbell rear delt fly",                        "gif_url": "https://v2.exercisedb.io/image/gifs/0356.gif"},
    {"name": "Upright Row",           "category": "strength",    "muscle_group": "shoulders", "description": "Barbell or dumbbell upright row",               "gif_url": "https://v2.exercisedb.io/image/gifs/0087.gif"},
    {"name": "Shrugs",                "category": "strength",    "muscle_group": "shoulders", "description": "Barbell or dumbbell shrugs for traps",          "gif_url": "https://v2.exercisedb.io/image/gifs/0077.gif"},

    # ── Arms ───────────────────────────────────────────────────────────
    {"name": "Barbell Curl",          "category": "strength",    "muscle_group": "arms",      "description": "Standing barbell bicep curl",                   "gif_url": "https://v2.exercisedb.io/image/gifs/0021.gif"},
    {"name": "Dumbbell Curl",         "category": "strength",    "muscle_group": "arms",      "description": "Alternating dumbbell bicep curl",               "gif_url": "https://v2.exercisedb.io/image/gifs/0320.gif"},
    {"name": "Hammer Curl",           "category": "strength",    "muscle_group": "arms",      "description": "Neutral grip dumbbell curl",                    "gif_url": "https://v2.exercisedb.io/image/gifs/0375.gif"},
    {"name": "Preacher Curl",         "category": "strength",    "muscle_group": "arms",      "description": "Barbell curl on preacher bench",                "gif_url": "https://v2.exercisedb.io/image/gifs/0068.gif"},
    {"name": "Cable Curl",            "category": "strength",    "muscle_group": "arms",      "description": "Standing cable bicep curl",                     "gif_url": "https://v2.exercisedb.io/image/gifs/0255.gif"},
    {"name": "Tricep Pushdown",       "category": "strength",    "muscle_group": "arms",      "description": "Cable tricep pushdown",                         "gif_url": "https://v2.exercisedb.io/image/gifs/0085.gif"},
    {"name": "Skull Crushers",        "category": "strength",    "muscle_group": "arms",      "description": "Lying barbell or EZ-bar tricep extension",      "gif_url": "https://v2.exercisedb.io/image/gifs/0045.gif"},
    {"name": "Overhead Tricep Extension", "category": "strength","muscle_group": "arms",      "description": "Dumbbell overhead tricep extension",            "gif_url": "https://v2.exercisedb.io/image/gifs/0344.gif"},
    {"name": "Close Grip Bench Press","category": "strength",    "muscle_group": "arms",      "description": "Close grip barbell bench for triceps",          "gif_url": "https://v2.exercisedb.io/image/gifs/0024.gif"},
    {"name": "Diamond Push-up",       "category": "strength",    "muscle_group": "arms",      "description": "Close grip push-up for triceps",               "gif_url": "https://v2.exercisedb.io/image/gifs/1169.gif"},

    # ── Legs ───────────────────────────────────────────────────────────
    {"name": "Squat",                 "category": "strength",    "muscle_group": "legs",      "description": "Barbell back squat",                            "gif_url": "https://v2.exercisedb.io/image/gifs/0080.gif"},
    {"name": "Front Squat",           "category": "strength",    "muscle_group": "legs",      "description": "Barbell front squat",                           "gif_url": "https://v2.exercisedb.io/image/gifs/0371.gif"},
    {"name": "Leg Press",             "category": "strength",    "muscle_group": "legs",      "description": "Machine leg press",                             "gif_url": "https://v2.exercisedb.io/image/gifs/0043.gif"},
    {"name": "Romanian Deadlift",     "category": "strength",    "muscle_group": "legs",      "description": "Barbell Romanian deadlift for hamstrings",      "gif_url": "https://v2.exercisedb.io/image/gifs/0176.gif"},
    {"name": "Lunges",                "category": "strength",    "muscle_group": "legs",      "description": "Barbell or dumbbell lunges",                    "gif_url": "https://v2.exercisedb.io/image/gifs/0358.gif"},
    {"name": "Bulgarian Split Squat", "category": "strength",    "muscle_group": "legs",      "description": "Rear foot elevated split squat",               "gif_url": "https://v2.exercisedb.io/image/gifs/1460.gif"},
    {"name": "Leg Curl",              "category": "strength",    "muscle_group": "legs",      "description": "Machine lying or seated leg curl",             "gif_url": "https://v2.exercisedb.io/image/gifs/0044.gif"},
    {"name": "Leg Extension",         "category": "strength",    "muscle_group": "legs",      "description": "Machine leg extension for quads",              "gif_url": "https://v2.exercisedb.io/image/gifs/0042.gif"},
    {"name": "Calf Raise",            "category": "strength",    "muscle_group": "legs",      "description": "Standing or seated calf raise",                "gif_url": "https://v2.exercisedb.io/image/gifs/0177.gif"},
    {"name": "Hack Squat",            "category": "strength",    "muscle_group": "legs",      "description": "Machine hack squat",                           "gif_url": "https://v2.exercisedb.io/image/gifs/0391.gif"},
    {"name": "Step-up",               "category": "strength",    "muscle_group": "legs",      "description": "Dumbbell step-up onto bench",                  "gif_url": "https://v2.exercisedb.io/image/gifs/0648.gif"},
    {"name": "Hip Thrust",            "category": "strength",    "muscle_group": "legs",      "description": "Barbell hip thrust for glutes",                "gif_url": "https://v2.exercisedb.io/image/gifs/1381.gif"},
    {"name": "Glute Bridge",          "category": "strength",    "muscle_group": "legs",      "description": "Bodyweight or loaded glute bridge",            "gif_url": "https://v2.exercisedb.io/image/gifs/0585.gif"},
    {"name": "Sumo Deadlift",         "category": "strength",    "muscle_group": "legs",      "description": "Wide stance sumo deadlift",                    "gif_url": "https://v2.exercisedb.io/image/gifs/0082.gif"},

    # ── Core ───────────────────────────────────────────────────────────
    {"name": "Plank",                 "category": "flexibility", "muscle_group": "core",      "description": "Static core hold",                             "gif_url": "https://v2.exercisedb.io/image/gifs/0536.gif"},
    {"name": "Crunch",                "category": "strength",    "muscle_group": "core",      "description": "Basic abdominal crunch",                       "gif_url": "https://v2.exercisedb.io/image/gifs/0027.gif"},
    {"name": "Sit-up",                "category": "strength",    "muscle_group": "core",      "description": "Full range sit-up",                            "gif_url": "https://v2.exercisedb.io/image/gifs/0078.gif"},
    {"name": "Leg Raise",             "category": "strength",    "muscle_group": "core",      "description": "Hanging or lying leg raise",                   "gif_url": "https://v2.exercisedb.io/image/gifs/0040.gif"},
    {"name": "Russian Twist",         "category": "strength",    "muscle_group": "core",      "description": "Weighted or bodyweight Russian twist",         "gif_url": "https://v2.exercisedb.io/image/gifs/0573.gif"},
    {"name": "Ab Wheel Rollout",      "category": "strength",    "muscle_group": "core",      "description": "Ab wheel rollout from knees or standing",      "gif_url": "https://v2.exercisedb.io/image/gifs/0001.gif"},
    {"name": "Cable Crunch",          "category": "strength",    "muscle_group": "core",      "description": "Kneeling cable crunch",                        "gif_url": "https://v2.exercisedb.io/image/gifs/0252.gif"},
    {"name": "Mountain Climber",      "category": "cardio",      "muscle_group": "core",      "description": "Dynamic mountain climber",                     "gif_url": "https://v2.exercisedb.io/image/gifs/0519.gif"},
    {"name": "Side Plank",            "category": "flexibility", "muscle_group": "core",      "description": "Lateral static core hold",                     "gif_url": "https://v2.exercisedb.io/image/gifs/0577.gif"},

    # ── Cardio ─────────────────────────────────────────────────────────
    {"name": "Running",               "category": "cardio",      "muscle_group": "full body", "description": "Outdoor or treadmill running",                 "gif_url": "https://v2.exercisedb.io/image/gifs/3220.gif"},
    {"name": "Cycling",               "category": "cardio",      "muscle_group": "legs",      "description": "Bike or stationary cycle",                     "gif_url": "https://v2.exercisedb.io/image/gifs/1160.gif"},
    {"name": "Jump Rope",             "category": "cardio",      "muscle_group": "full body", "description": "Skipping rope",                                "gif_url": "https://v2.exercisedb.io/image/gifs/3636.gif"},
    {"name": "Rowing Machine",        "category": "cardio",      "muscle_group": "full body", "description": "Cardio rowing machine",                        "gif_url": "https://v2.exercisedb.io/image/gifs/2628.gif"},
    {"name": "Elliptical",            "category": "cardio",      "muscle_group": "full body", "description": "Elliptical cross trainer",                     "gif_url": "https://v2.exercisedb.io/image/gifs/3223.gif"},
    {"name": "Stair Climber",         "category": "cardio",      "muscle_group": "legs",      "description": "Stair climber machine",                        "gif_url": "https://v2.exercisedb.io/image/gifs/3224.gif"},
    {"name": "Burpees",               "category": "cardio",      "muscle_group": "full body", "description": "Full body burpee",                             "gif_url": "https://v2.exercisedb.io/image/gifs/0025.gif"},
    {"name": "Jumping Jacks",         "category": "cardio",      "muscle_group": "full body", "description": "Classic jumping jacks",                        "gif_url": "https://v2.exercisedb.io/image/gifs/3317.gif"},
    {"name": "Box Jump",              "category": "cardio",      "muscle_group": "legs",      "description": "Explosive jump onto a box",                    "gif_url": "https://v2.exercisedb.io/image/gifs/0194.gif"},
    {"name": "Battle Ropes",          "category": "cardio",      "muscle_group": "full body", "description": "Heavy rope wave exercises",                    "gif_url": "https://v2.exercisedb.io/image/gifs/0148.gif"},
    {"name": "Swimming",              "category": "cardio",      "muscle_group": "full body", "description": "Pool or open water swimming",                  "gif_url": None},
    {"name": "Sprint Intervals",      "category": "cardio",      "muscle_group": "full body", "description": "High intensity sprint intervals",              "gif_url": None},

    # ── Flexibility ────────────────────────────────────────────────────
    {"name": "Hip Flexor Stretch",    "category": "flexibility", "muscle_group": "hips",      "description": "Kneeling hip flexor stretch",                  "gif_url": "https://v2.exercisedb.io/image/gifs/0566.gif"},
    {"name": "Hamstring Stretch",     "category": "flexibility", "muscle_group": "legs",      "description": "Standing or seated hamstring stretch",         "gif_url": "https://v2.exercisedb.io/image/gifs/0397.gif"},
    {"name": "Quad Stretch",          "category": "flexibility", "muscle_group": "legs",      "description": "Standing quad stretch",                        "gif_url": None},
    {"name": "Chest Stretch",         "category": "flexibility", "muscle_group": "chest",     "description": "Doorway or band chest stretch",                "gif_url": None},
    {"name": "Child's Pose",          "category": "flexibility", "muscle_group": "back",      "description": "Yoga child's pose for back and hips",          "gif_url": "https://v2.exercisedb.io/image/gifs/2466.gif"},
    {"name": "Cat-Cow Stretch",       "category": "flexibility", "muscle_group": "back",      "description": "Spinal mobility stretch",                      "gif_url": "https://v2.exercisedb.io/image/gifs/2467.gif"},
    {"name": "Pigeon Pose",           "category": "flexibility", "muscle_group": "hips",      "description": "Deep hip opener stretch",                      "gif_url": None},
    {"name": "Shoulder Cross Stretch","category": "flexibility", "muscle_group": "shoulders", "description": "Cross-body shoulder stretch",                  "gif_url": None},
    {"name": "Tricep Stretch",        "category": "flexibility", "muscle_group": "arms",      "description": "Overhead tricep and shoulder stretch",         "gif_url": None},
    {"name": "Calf Stretch",          "category": "flexibility", "muscle_group": "legs",      "description": "Wall calf stretch",                            "gif_url": None},
]

def seed_exercises(db=None):
    close_after = False
    if db is None:
        from app.db.session import SessionLocal
        db = SessionLocal()
        close_after = True
    try:
        added = 0
        updated = 0
        for data in EXERCISES:
            existing = db.query(Exercise).filter_by(name=data["name"]).first()
            if not existing:
                db.add(Exercise(**data))
                added += 1
            elif not existing.gif_url and data.get("gif_url"):
                existing.gif_url = data["gif_url"]
                updated += 1
        db.commit()
        print(f"Seeded {added} new exercises, updated {updated} GIF URLs ({len(EXERCISES)} total).")
    finally:
        if close_after:
            db.close()