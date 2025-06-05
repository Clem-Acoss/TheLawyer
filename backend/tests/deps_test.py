import pytest
import uuid
from fastapi import HTTPException
from jose import jwt
from sqlalchemy.orm import Session
from app.auth import deps
from app.models import User
from app.config import SECRET_KEY, ALGORITHM


def create_token(user_id: int):
    from datetime import datetime, timedelta
    expire = datetime.utcnow() + timedelta(minutes=5)
    to_encode = {"sub": str(user_id), "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def test_get_db_yields_and_closes():
    gen = deps.get_db()
    db = next(gen)
    assert db is not None
    gen.close()  # Le finally doit fermer la session sans erreur


def test_get_current_user_valid_token(session: Session):
    # Générer un email unique pour éviter les collisions
    unique_email = f"{uuid.uuid4()}@example.com"

    user = User(email=unique_email, hashed_password="hashed")
    session.add(user)
    session.commit()
    session.refresh(user)

    token = create_token(user.id)

    result = deps.get_current_user(token=token, db=session)
    assert result.id == user.id
    assert result.email == user.email


def test_get_current_user_invalid_token(session: Session):
    invalid_token = "invalid.token.here"
    with pytest.raises(HTTPException) as exc_info:
        deps.get_current_user(token=invalid_token, db=session)
    assert exc_info.value.status_code == 401


def test_get_current_user_user_not_found(session: Session):
    token = create_token(99999)  # Un ID utilisateur inexistant
    with pytest.raises(HTTPException) as exc_info:
        deps.get_current_user(token=token, db=session)
    assert exc_info.value.status_code == 401
