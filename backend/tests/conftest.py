import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app
from app.auth.utils import create_access_token
from app import models
from app.auth.deps import get_db

# Crée une BDD SQLite en mémoire (ou sur disque temporaire si besoin)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Pour debug, sinon "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crée toutes les tables une seule fois
@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Fournit une session DB isolée pour chaque test
@pytest.fixture(scope="function")
def session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Remplace le get_db de FastAPI par la session test
@pytest.fixture(scope="function", autouse=True)
def override_get_db(session):
    def _get_db_override():
        yield session
    app.dependency_overrides[get_db] = _get_db_override

# Client FastAPI avec dépendances surchargées
@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c

# Crée un utilisateur de test + token pour les routes protégées
@pytest.fixture
def user_token(session):
    user = models.User(email="user@example.com", hashed_password="fakehashed")
    session.add(user)
    session.commit()
    session.refresh(user)
    token = create_access_token({"sub": str(user.id)})
    return token, user

# En-tête d'autorisation pour les requêtes
@pytest.fixture
def auth_header(user_token):
    token, _ = user_token
    return {"Authorization": f"Bearer {token}"}
