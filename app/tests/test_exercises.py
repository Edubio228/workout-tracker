import pytest

@pytest.fixture
def custom_exercise():
    return {
        "name": "Cable Fly",
        "category": "strength",
        "muscle_group": "chest",
        "description": "Cable crossover fly"
    }

def test_list_exercises_includes_seeded(auth_client):
    response = auth_client.get("/exercises/")
    assert response.status_code == 200
    assert len(response.json()) >= 10  # seeded exercises

def test_list_exercises_unauthenticated(client):
    response = client.get("/exercises/")
    assert response.status_code == 401

def test_create_custom_exercise(auth_client, custom_exercise):
    response = auth_client.post("/exercises/", json=custom_exercise)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Cable Fly"
    assert data["user_id"] is not None  # owned by user, not global

def test_create_duplicate_exercise(auth_client, custom_exercise):
    auth_client.post("/exercises/", json=custom_exercise)
    response = auth_client.post("/exercises/", json=custom_exercise)
    assert response.status_code == 400

def test_custom_exercise_appears_in_list(auth_client, custom_exercise):
    auth_client.post("/exercises/", json=custom_exercise)
    response = auth_client.get("/exercises/")
    names = [e["name"] for e in response.json()]
    assert "Cable Fly" in names

def test_update_custom_exercise(auth_client, custom_exercise):
    created = auth_client.post("/exercises/", json=custom_exercise).json()
    response = auth_client.patch(f"/exercises/{created['id']}", json={
        "name": "Cable Crossover"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Cable Crossover"

def test_cannot_edit_global_exercise(auth_client):
    exercises = auth_client.get("/exercises/").json()
    global_ex = next(e for e in exercises if e["user_id"] is None)
    response = auth_client.patch(f"/exercises/{global_ex['id']}", json={
        "name": "Hacked Exercise"
    })
    assert response.status_code == 403

def test_delete_custom_exercise(auth_client, custom_exercise):
    created = auth_client.post("/exercises/", json=custom_exercise).json()
    delete_response = auth_client.delete(f"/exercises/{created['id']}")
    assert delete_response.status_code == 204

def test_cannot_delete_global_exercise(auth_client):
    exercises = auth_client.get("/exercises/").json()
    global_ex = next(e for e in exercises if e["user_id"] is None)
    response = auth_client.delete(f"/exercises/{global_ex['id']}")
    assert response.status_code == 403

def test_filter_by_category(auth_client):
    response = auth_client.get("/exercises/?category=cardio")
    assert response.status_code == 200
    assert all(e["category"] == "cardio" for e in response.json())

def test_filter_by_muscle_group(auth_client):
    response = auth_client.get("/exercises/?muscle_group=chest")
    assert response.status_code == 200
    assert all(e["muscle_group"] == "chest" for e in response.json())

def test_custom_exercise_not_visible_to_other_user(client, custom_exercise):
    """User B should not see User A's custom exercises."""
    client.post("/auth/register", json={
        "username": "userA", "email": "a@example.com", "password": "password123"
    })
    token_a = client.post("/auth/login", data={
        "username": "userA", "password": "password123"
    }).json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token_a}"})
    client.post("/exercises/", json=custom_exercise)

    client.post("/auth/register", json={
        "username": "userB", "email": "b@example.com", "password": "password123"
    })
    token_b = client.post("/auth/login", data={
        "username": "userB", "password": "password123"
    }).json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token_b}"})

    response = client.get("/exercises/")
    names = [e["name"] for e in response.json()]
    assert "Cable Fly" not in names