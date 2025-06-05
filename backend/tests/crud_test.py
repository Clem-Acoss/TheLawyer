import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.schemas import UserCreate, ConversationCreate, MessageCreate
from app.crud import (
    create_user, get_user_by_email, authenticate_user, get_user_by_id,
    create_conversation, get_conversations_by_user, get_conversation_by_id, delete_conversation,
    create_message, get_messages_by_conversation
)

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def test_user_crud(db_session):
    user_in = UserCreate(email="test@example.com", password="mypassword")

    user = create_user(db_session, user_in)
    assert user.id is not None
    assert user.email == "test@example.com"

    user2 = get_user_by_email(db_session, "test@example.com")
    assert user2.email == user.email

    auth_user = authenticate_user(db_session, "test@example.com", "mypassword")
    assert auth_user is not None
    assert auth_user.email == "test@example.com"

    auth_fail = authenticate_user(db_session, "test@example.com", "wrongpass")
    assert auth_fail is None

    user_by_id = get_user_by_id(db_session, user.id)
    assert user_by_id.email == user.email


def test_conversation_crud(db_session):
    user = create_user(db_session, UserCreate(email="convuser@example.com", password="pass"))

    conv_in = ConversationCreate(title="Ma conversation")
    conv = create_conversation(db_session, conv_in, user.id)
    assert conv.id is not None
    assert conv.title == "Ma conversation"
    assert conv.user_id == user.id

    convs = get_conversations_by_user(db_session, user.id)
    assert len(convs) == 1
    assert convs[0].title == "Ma conversation"

    conv_by_id = get_conversation_by_id(db_session, conv.id)
    assert conv_by_id.title == "Ma conversation"

    deleted = delete_conversation(db_session, conv.id, user.id)
    assert deleted is True

    deleted_again = delete_conversation(db_session, conv.id, user.id)
    assert deleted_again is False


def test_message_crud(db_session):
    user = create_user(db_session, UserCreate(email="msguser@example.com", password="pass"))
    conv = create_conversation(db_session, ConversationCreate(title="Conv pour messages"), user.id)

    msg_in = MessageCreate(conversation_id=conv.id, sender="user", content="Hello IA")
    msg = create_message(db_session, msg_in)
    assert msg.id is not None
    assert msg.content == "Hello IA"
    assert msg.conversation_id == conv.id

    msgs = get_messages_by_conversation(db_session, conv.id)
    assert len(msgs) == 1
    assert msgs[0].content == "Hello IA"
