from fastapi import status
import pytest
from models import User

def test_register_user(client, session):
    # Ensure user doesn't exist (it shouldn't in a fresh in-memory db, or separate test function)
    # Using 'session' fixture ensures isolation usually if configured right.
    
    response = client.post("/users/", json={
        "email": "newuser@example.com",
        "password": "newpassword123",
        "gender": "female",
        "weight": 60,
        "height": 165,
        "age": 28,
        "activity_level": "sedentary",
        "goal": "maintain"
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert "id" in data
    assert "hashed_password" not in data

def test_register_existing_user(client, test_user):
    response = client.post("/users/", json={
        "email": test_user.email, # Object access
        "password": "somepassword",
        "gender": "male",
        "weight": 70,
        "height": 170,
        "age": 20,
        "activity_level": "light",
        "goal": "gain"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_login_success(client, test_user):
    response = client.post("/token", data={
        "username": test_user.email,
        "password": "testpassword" # Matches fixture
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_failure(client, test_user):
    response = client.post("/token", data={
        "username": test_user.email,
        "password": "wrongpassword"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_current_user(client, auth_headers, test_user):
    response = client.get("/users/me/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user.email

def test_get_current_user_unauthorized(client):
    response = client.get("/users/me/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
