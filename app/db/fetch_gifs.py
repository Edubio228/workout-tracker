import requests
from app.db.session import SessionLocal
from app.models.exercise import Exercise
import app.models.user    # noqa — must import so SQLAlchemy sees User
import app.models.workout # noqa — must import so SQLAlchemy sees Workout

RAPIDAPI_KEY = "07b8b11baamshbcae68fbffc42f6p124104jsnbbcd6039a14d"

EXERCISE_DB_NAMES = {
    "Bench Press":            "barbell bench press",
    "Incline Bench Press":    "incline barbell bench press",
    "Squat":                  "barbell squat",
    "Deadlift":               "deadlift",
    "Pull-up":                "pull-up",
    "Overhead Press":         "barbell overhead press",
    "Barbell Row":            "barbell bent over row",
    "Dumbbell Curl":          "dumbbell bicep curl",
    "Tricep Pushdown":        "cable pushdown",
    "Lateral Raise":          "dumbbell lateral raise",
    "Leg Press":              "leg press",
    "Romanian Deadlift":      "romanian deadlift",
    "Hip Thrust":             "barbell hip thrust",
    "Plank":                  "plank",
    "Running":                "run",
}

def fetch_gif_url(exercise_name: str) -> str | None:
    url = "https://exercisedb.p.rapidapi.com/exercises/name/" + exercise_name.lower()
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
    }
    try:
        res = requests.get(url, headers=headers, timeout=10)
        data = res.json()
        if data and isinstance(data, list) and len(data) > 0:
            return data[0].get("gifUrl")
    except Exception as e:
        print(f"Error fetching {exercise_name}: {e}")
    return None

def populate_gifs():
    db = SessionLocal()
    try:
        for our_name, search_name in EXERCISE_DB_NAMES.items():
            exercise = db.query(Exercise).filter_by(name=our_name).first()
            if exercise and not exercise.gif_url:
                gif_url = fetch_gif_url(search_name)
                if gif_url:
                    exercise.gif_url = gif_url
                    print(f"✓ Added GIF for {our_name}")
                else:
                    print(f"✗ No GIF found for {our_name}")
            elif exercise and exercise.gif_url:
                print(f"- Already has GIF: {our_name}")
            else:
                print(f"? Exercise not found in DB: {our_name}")
        db.commit()
        print("Done.")
    finally:
        db.close()

if __name__ == "__main__":
    populate_gifs()