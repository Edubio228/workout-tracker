def test_workout_pagination(auth_client):
    for i in range(5):
        auth_client.post("/workouts/", json={
            "title": f"Workout {i}",
            "scheduled_at": f"2026-04-0{i+1}T10:00:00",
            "exercises": []
        })
    response = auth_client.get("/workouts/?skip=0&limit=3")
    assert response.status_code == 200
    assert len(response.json()) == 3

    response = auth_client.get("/workouts/?skip=3&limit=3")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_workout_pagination_default_limit(auth_client):
    for i in range(5):
        auth_client.post("/workouts/", json={
            "title": f"Workout {i}",
            "scheduled_at": f"2026-04-0{i+1}T10:00:00",
            "exercises": []
        })
    response = auth_client.get("/workouts/")
    assert response.status_code == 200
    assert len(response.json()) == 5

def test_workout_pagination_limit_too_high(auth_client):
    response = auth_client.get("/workouts/?limit=999")
    assert response.status_code == 422  # validation error

def test_workout_pagination_negative_skip(auth_client):
    response = auth_client.get("/workouts/?skip=-1")
    assert response.status_code == 422

def test_exercises_pagination(auth_client):
    response = auth_client.get("/exercises/?skip=0&limit=5")
    assert response.status_code == 200
    assert len(response.json()) <= 5

def test_templates_pagination(auth_client):
    for i in range(4):
        auth_client.post("/templates/", json={"title": f"Template {i}", "exercises": []})
    response = auth_client.get("/templates/?skip=0&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_body_measurements_pagination(auth_client):
    for i in range(5):
        auth_client.post("/body/", json={"weight_kg": 80.0 + i})
    response = auth_client.get("/body/?skip=0&limit=3")
    assert response.status_code == 200
    assert len(response.json()) == 3