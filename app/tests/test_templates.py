import pytest

@pytest.fixture
def sample_template():
    return {
        "title": "Push Day",
        "notes": "Chest, shoulders, triceps",
        "exercises": []
    }

def test_create_template(auth_client, sample_template):
    response = auth_client.post("/templates/", json=sample_template)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Push Day"
    assert "id" in data

def test_create_template_unauthenticated(client, sample_template):
    response = client.post("/templates/", json=sample_template)
    assert response.status_code == 401

def test_list_templates(auth_client, sample_template):
    auth_client.post("/templates/", json=sample_template)
    auth_client.post("/templates/", json={**sample_template, "title": "Pull Day"})
    response = auth_client.get("/templates/")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_template(auth_client, sample_template):
    created = auth_client.post("/templates/", json=sample_template).json()
    response = auth_client.get(f"/templates/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]

def test_get_template_not_found(auth_client):
    response = auth_client.get("/templates/99999")
    assert response.status_code == 404

def test_update_template(auth_client, sample_template):
    created = auth_client.post("/templates/", json=sample_template).json()
    response = auth_client.patch(f"/templates/{created['id']}", json={"title": "Heavy Push Day"})
    assert response.status_code == 200
    assert response.json()["title"] == "Heavy Push Day"

def test_delete_template(auth_client, sample_template):
    created = auth_client.post("/templates/", json=sample_template).json()
    delete_response = auth_client.delete(f"/templates/{created['id']}")
    assert delete_response.status_code == 204
    get_response = auth_client.get(f"/templates/{created['id']}")
    assert get_response.status_code == 404

def test_spawn_workout_from_template(auth_client, sample_template):
    created = auth_client.post("/templates/", json=sample_template).json()
    response = auth_client.post(f"/templates/{created['id']}/spawn", json={
        "scheduled_at": "2026-04-10T09:00:00"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Push Day"
    assert data["status"] == "pending"
    assert data["scheduled_at"] is not None

def test_spawn_creates_independent_workout(auth_client, sample_template):
    """Deleting the template should not delete spawned workouts."""
    created = auth_client.post("/templates/", json=sample_template).json()
    workout = auth_client.post(f"/templates/{created['id']}/spawn", json={}).json()
    auth_client.delete(f"/templates/{created['id']}")
    response = auth_client.get(f"/workouts/{workout['id']}")
    assert response.status_code == 200