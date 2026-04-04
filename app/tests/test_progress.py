import pytest
from datetime import datetime, timedelta


@pytest.fixture
def completed_workout(auth_client):
    """Creates a completed workout with one exercise."""
    exercises = auth_client.get("/exercises/").json()
    bench = next(e for e in exercises if e["name"] == "Bench Press")

    workout = auth_client.post("/workouts/", json={
        "title": "Chest Day",
        "scheduled_at": datetime.utcnow().isoformat(),
        "exercises": [
            {
                "exercise_id": bench["id"],
                "sets": 4,
                "reps": 8,
                "weight_kg": 80.0,
            }
        ]
    }).json()

    auth_client.patch(f"/workouts/{workout['id']}", json={"status": "completed"})
    return {"workout": workout, "exercise": bench}


def test_exercise_progress_empty(auth_client):
    exercises = auth_client.get("/exercises/").json()
    bench = next(e for e in exercises if e["name"] == "Bench Press")
    response = auth_client.get(f"/progress/exercise/{bench['id']}")
    assert response.status_code == 200
    assert response.json()["data"] == []


def test_exercise_progress_has_data(auth_client, completed_workout):
    exercise_id = completed_workout["exercise"]["id"]
    response = auth_client.get(f"/progress/exercise/{exercise_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["exercise_name"] == "Bench Press"
    assert len(data["data"]) == 1
    assert data["data"][0]["best_weight_kg"] == 80.0
    assert data["data"][0]["best_reps"] == 8


def test_exercise_progress_multiple_sessions(auth_client):
    """Later sessions with heavier weight should show progression."""
    exercises = auth_client.get("/exercises/").json()
    bench = next(e for e in exercises if e["name"] == "Bench Press")

    for weight in [60.0, 70.0, 80.0]:
        workout = auth_client.post("/workouts/", json={
            "title": f"Chest Day {weight}kg",
            "scheduled_at": datetime.utcnow().isoformat(),
            "exercises": [
                {"exercise_id": bench["id"], "sets": 3, "reps": 8, "weight_kg": weight}
            ]
        }).json()
        auth_client.patch(f"/workouts/{workout['id']}", json={"status": "completed"})

    response = auth_client.get(f"/progress/exercise/{bench['id']}")
    data = response.json()["data"]
    assert len(data) == 3
    weights = [d["best_weight_kg"] for d in data]
    assert weights == [60.0, 70.0, 80.0]


def test_volume_empty(auth_client):
    response = auth_client.get("/progress/volume")
    assert response.status_code == 200
    assert response.json()["data"] == []


def test_volume_has_data(auth_client, completed_workout):
    response = auth_client.get("/progress/volume")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 1
    # 4 sets x 8 reps x 80kg = 2560kg
    assert data[0]["volume_kg"] == 2560.0


def test_workout_frequency_empty(auth_client):
    response = auth_client.get("/progress/workouts")
    assert response.status_code == 200
    assert response.json()["data"] == []


def test_workout_frequency_has_data(auth_client, completed_workout):
    response = auth_client.get("/progress/workouts")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 1
    assert data[0]["workouts_completed"] == 1


def test_progress_respects_days_filter(auth_client):
    """Workouts outside the day range should not appear."""
    exercises = auth_client.get("/exercises/").json()
    bench = next(e for e in exercises if e["name"] == "Bench Press")

    old_date = (datetime.utcnow() - timedelta(days=120)).isoformat()
    workout = auth_client.post("/workouts/", json={
        "title": "Old Workout",
        "scheduled_at": old_date,
        "exercises": [
            {"exercise_id": bench["id"], "sets": 3, "reps": 8, "weight_kg": 60.0}
        ]
    }).json()
    auth_client.patch(f"/workouts/{workout['id']}", json={"status": "completed"})

    response = auth_client.get(f"/progress/exercise/{bench['id']}?days=90")
    assert response.json()["data"] == []