import pytest
import uuid
from sqlalchemy.orm import Session
from app.chat import service
from app import models


@pytest.fixture
def fake_db(session: Session):
    return session


@pytest.fixture
def fake_user(fake_db: Session):
    # Génère un email unique à chaque test
    unique_email = f"{uuid.uuid4()}@example.com"
    user = models.User(email=unique_email, hashed_password="hashed")
    fake_db.add(user)
    fake_db.commit()
    fake_db.refresh(user)
    return user


def test_create_conversation(fake_db: Session, fake_user: models.User):
    title = "Ma première conversation"
    conv = service.create_conversation(fake_db, user_id=fake_user.id, title=title)
    assert conv.title == title
    assert conv.user_id == fake_user.id


def test_get_conversations(fake_db: Session, fake_user: models.User):
    service.create_conversation(fake_db, user_id=fake_user.id, title="Conv 1")
    service.create_conversation(fake_db, user_id=fake_user.id, title="Conv 2")

    convs = service.get_conversations(fake_db, user_id=fake_user.id)
    assert len(convs) == 2
    assert all(c.title.startswith("Conv") for c in convs)


def test_add_and_get_messages(fake_db: Session, fake_user: models.User):
    conv = service.create_conversation(fake_db, user_id=fake_user.id, title="Chat")
    service.add_message(fake_db, conv.id, "user", "Bonjour", is_ai=False)
    service.add_message(fake_db, conv.id, "ai", "Salut, humain", is_ai=True)

    messages = service.get_messages(fake_db, conversation_id=conv.id)
    assert len(messages) == 2
    assert messages[0].sender == "user"
    assert messages[1].is_ai is True
