import pytest

@pytest.fixture
def sample_workout():
    """A reusable workout payload."""
    return {
        "title": "Chest Day",
        "notes": "Focus on form",
        "scheduled_at": "2026-04-02T10:00:00",
        "exercises": []
    }

def test_create_workout(auth_client, sample_workout):
    response = auth_client.post("/workouts/", json=sample_workout)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Chest Day"
    assert data["status"] == "pending"
    assert "id" in data

def test_create_workout_unauthenticated(client, sample_workout):
    response = client.post("/workouts/", json=sample_workout)
    assert response.status_code == 401

def test_list_workouts_empty(auth_client):
    response = auth_client.get("/workouts/")
    assert response.status_code == 200
    assert response.json() == []

def test_list_workouts(auth_client, sample_workout):
    auth_client.post("/workouts/", json=sample_workout)
    auth_client.post("/workouts/", json={**sample_workout, "title": "Leg Day"})
    response = auth_client.get("/workouts/")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_workout(auth_client, sample_workout):
    created = auth_client.post("/workouts/", json=sample_workout).json()
    response = auth_client.get(f"/workouts/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]

def test_get_workout_not_found(auth_client):
    response = auth_client.get("/workouts/99999")
    assert response.status_code == 404

def test_update_workout(auth_client, sample_workout):
    created = auth_client.post("/workouts/", json=sample_workout).json()
    response = auth_client.patch(f"/workouts/{created['id']}", json={
        "title": "Updated Title",
        "notes": "New notes"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

def test_complete_workout(auth_client, sample_workout):
    created = auth_client.post("/workouts/", json=sample_workout).json()
    response = auth_client.patch(f"/workouts/{created['id']}", json={
        "status": "completed"
    })
    assert response.status_code == 200
    assert response.json()["status"] == "completed"

def test_delete_workout(auth_client, sample_workout):
    created = auth_client.post("/workouts/", json=sample_workout).json()
    delete_response = auth_client.delete(f"/workouts/{created['id']}")
    assert delete_response.status_code == 204
    # Confirm it's gone
    get_response = auth_client.get(f"/workouts/{created['id']}")
    assert get_response.status_code == 404

def test_cannot_access_other_users_workout(client, sample_workout):
    """User A should not be able to see User B's workouts."""
    # Register and log in as User A
    client.post("/auth/register", json={
        "username": "userA", "email": "a@example.com", "password": "password123"
    })
    login_a = client.post("/auth/login", data={"username": "userA", "password": "password123"})
    token_a = login_a.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token_a}"})
    workout = client.post("/workouts/", json=sample_workout).json()

    # Log in as User B
    client.post("/auth/register", json={
        "username": "userB", "email": "b@example.com", "password": "password123"
    })
    login_b = client.post("/auth/login", data={"username": "userB", "password": "password123"})
    token_b = login_b.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token_b}"})

    # User B tries to access User A's workout
    response = client.get(f"/workouts/{workout['id']}")
    assert response.status_code == 404