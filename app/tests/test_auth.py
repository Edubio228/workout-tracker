def test_register_success(client):
    response = client.post("/auth/register", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "new@example.com"
    assert "password" not in data        # never expose password
    assert "password_hash" not in data   # never expose hash either

def test_register_duplicate_email(client):
    client.post("/auth/register", json={
        "username": "user1",
        "email": "same@example.com",
        "password": "password123"
    })
    response = client.post("/auth/register", json={
        "username": "user2",
        "email": "same@example.com",
        "password": "password123"
    })
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

def test_register_duplicate_username(client):
    client.post("/auth/register", json={
        "username": "sameuser",
        "email": "first@example.com",
        "password": "password123"
    })
    response = client.post("/auth/register", json={
        "username": "sameuser",
        "email": "second@example.com",
        "password": "password123"
    })
    assert response.status_code == 400

def test_login_success(client, registered_user):
    response = client.post("/auth/login", data={
        "username": registered_user["username"],
        "password": registered_user["password"],
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, registered_user):
    response = client.post("/auth/login", data={
        "username": registered_user["username"],
        "password": "wrongpassword",
    })
    assert response.status_code == 401

def test_login_wrong_username(client):
    response = client.post("/auth/login", data={
        "username": "nobody",
        "password": "password123",
    })
    assert response.status_code == 401