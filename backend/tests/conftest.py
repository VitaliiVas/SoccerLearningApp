import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth import get_current_user
from app.database import Base, get_db
from app.main import app

# Import all models so their tables register with Base.metadata
from app import models  # noqa: F401

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    expire_on_commit=False,
)

TEST_CLERK_ID = "test_clerk_user_123"


def fake_current_user() -> str:
    return TEST_CLERK_ID


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)

    app.dependency_overrides[get_current_user] = fake_current_user
    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_current_user, None)
        app.dependency_overrides.pop(get_db, None)
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session(client):
    # Depends on `client` so tables exist before the session is handed out.
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
