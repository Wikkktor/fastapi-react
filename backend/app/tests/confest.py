import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app
from db.base_class import Base
from api.deps import get_db

# Create a test database URL for PostgreSQL
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
# Set up the database engine for testing
engine = create_engine(TEST_DATABASE_URL)

# Create a testing session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency override for database
@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def db_session(db_engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    with SessionLocal() as session:
        yield session


# Override FastAPI's get_db dependency
@pytest.fixture(scope="class")
def override_get_db(db_session):
    def _get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.pop(get_db, None)


# Fixture for TestClient
@pytest.fixture(scope="class")
def client(override_get_db):
    with TestClient(app) as test_client:
        yield test_client
