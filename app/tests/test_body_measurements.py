import pytest
from datetime import datetime, timedelta


@pytest.fixture
def sample_entry():
    return {
        "weight_kg": 80.5,
        "body_fat_pct": 18.0,
        "waist_cm": 85.0,
        "notes": "Morning measurement"
    }


def test_log_measurement(auth_client, sample_entry):
    response = auth_client.post("/body/", json=sample_entry)
    assert response.status_code == 201
    data = response.json()
    assert data["weight_kg"] == 80.5
    assert data["body_fat_pct"] == 18.0
    assert data["waist_cm"] == 85.0
    assert "id" in data
    assert "logged_at" in data


def test_log_partial_measurement(auth_client):
    """Only weight — all other fields should be None."""
    response = auth_client.post("/body/", json={"weight_kg": 79.0})
    assert response.status_code == 201
    data = response.json()
    assert data["weight_kg"] == 79.0
    assert data["body_fat_pct"] is None
    assert data["waist_cm"] is None


def test_log_measurement_unauthenticated(client, sample_entry):
    response = client.post("/body/", json=sample_entry)
    assert response.status_code == 401


def test_list_measurements(auth_client, sample_entry):
    auth_client.post("/body/", json=sample_entry)
    auth_client.post("/body/", json={"weight_kg": 80.0})
    response = auth_client.get("/body/")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_measurements_empty(auth_client):
    response = auth_client.get("/body/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_measurements_days_filter(auth_client):
    auth_client.post("/body/", json={
        "weight_kg": 82.0,
        "logged_at": (datetime.utcnow() - timedelta(days=120)).isoformat()
    })
    auth_client.post("/body/", json={"weight_kg": 80.0})
    response = auth_client.get("/body/?days=30")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["weight_kg"] == 80.0


def test_latest_measurement(auth_client):
    auth_client.post("/body/", json={"weight_kg": 82.0})
    auth_client.post("/body/", json={"weight_kg": 80.0})
    response = auth_client.get("/body/latest")
    assert response.status_code == 200
    assert response.json()["weight_kg"] == 80.0


def test_latest_measurement_not_found(auth_client):
    response = auth_client.get("/body/latest")
    assert response.status_code == 404


def test_measurement_stats(auth_client):
    auth_client.post("/body/", json={
        "weight_kg": 85.0,
        "waist_cm": 90.0,
        "logged_at": (datetime.utcnow() - timedelta(days=30)).isoformat()
    })
    auth_client.post("/body/", json={
        "weight_kg": 80.0,
        "waist_cm": 85.0,
    })
    response = auth_client.get("/body/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["stats"]["weight_kg"]["first"] == 85.0
    assert data["stats"]["weight_kg"]["latest"] == 80.0
    assert data["stats"]["weight_kg"]["change"] == -5.0
    assert data["stats"]["waist_cm"]["change"] == -5.0


def test_get_measurement(auth_client, sample_entry):
    created = auth_client.post("/body/", json=sample_entry).json()
    response = auth_client.get(f"/body/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_update_measurement(auth_client, sample_entry):
    created = auth_client.post("/body/", json=sample_entry).json()
    response = auth_client.patch(f"/body/{created['id']}", json={"weight_kg": 79.5})
    assert response.status_code == 200
    assert response.json()["weight_kg"] == 79.5


def test_delete_measurement(auth_client, sample_entry):
    created = auth_client.post("/body/", json=sample_entry).json()
    delete_response = auth_client.delete(f"/body/{created['id']}")
    assert delete_response.status_code == 204
    get_response = auth_client.get(f"/body/{created['id']}")
    assert get_response.status_code == 404


def test_cannot_access_other_users_measurements(client, sample_entry):
    client.post("/auth/register", json={
        "username": "userA", "email": "a@example.com", "password": "password123"
    })
    token_a = client.post("/auth/login", data={
        "username": "userA", "password": "password123"
    }).json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token_a}"})
    entry = client.post("/body/", json=sample_entry).json()

    client.post("/auth/register", json={
        "username": "userB", "email": "b@example.com", "password": "password123"
    })
    token_b = client.post("/auth/login", data={
        "username": "userB", "password": "password123"
    }).json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token_b}"})

    response = client.get(f"/body/{entry['id']}")
    assert response.status_code == 404