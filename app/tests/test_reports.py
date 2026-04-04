def test_summary_empty(auth_client):
    response = auth_client.get("/reports/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_workouts"] == 0
    assert data["completed"] == 0

def test_summary_counts(auth_client):
    workout1 = auth_client.post("/workouts/", json={
        "title": "W1", "scheduled_at": "2026-04-01T10:00:00", "exercises": []
    }).json()
    workout2 = auth_client.post("/workouts/", json={
        "title": "W2", "scheduled_at": "2026-04-02T10:00:00", "exercises": []
    }).json()

    auth_client.patch(f"/workouts/{workout1['id']}", json={"status": "completed"})
    auth_client.patch(f"/workouts/{workout2['id']}", json={"status": "skipped"})

    response = auth_client.get("/reports/summary")
    data = response.json()
    assert data["total_workouts"] == 2
    assert data["completed"] == 1
    assert data["skipped"] == 1