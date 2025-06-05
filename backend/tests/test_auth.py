import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import User
from app.auth.utils import hash_password
from sqlalchemy.orm import Session
from datetime import datetime

client = TestClient(app)

def test_signup_user_already_exists(session: Session):
    # Créer un utilisateur existant
    user = User(email="exists@example.com", hashed_password=hash_password("anypassword"))
    session.add(user)
    session.commit()

    response = client.post("/auth/signup", json={
        "email": "exists@example.com",
        "password": "anypassword"
    })

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_signup_new_user(session: Session):
    response = client.post("/auth/signup", json={
        "email": "new@example.com",
        "password": "strongpassword"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "new@example.com"
    assert "created_at" in data

    # Vérifier que l'utilisateur est bien en base
    user = session.query(User).filter_by(email="new@example.com").first()
    assert user is not None

def test_login_successful(session: Session):
    # Préparer un utilisateur
    user = User(email="login@example.com", hashed_password=hash_password("correctpassword"))
    session.add(user)
    session.commit()

    response = client.post("/auth/login", data={
        "username": "login@example.com",
        "password": "correctpassword"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_failure_wrong_password(session: Session):
    user = User(email="wrong@example.com", hashed_password=hash_password("correctpassword"))
    session.add(user)
    session.commit()

    response = client.post("/auth/login", data={
        "username": "wrong@example.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_login_failure_user_not_found(session: Session):
    response = client.post("/auth/login", data={
        "username": "nouser@example.com",
        "password": "any"
    })

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
