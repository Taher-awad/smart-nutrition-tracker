import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine, select
from sqlmodel.pool import StaticPool
from unittest.mock import patch, MagicMock

# Add backend to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app, get_current_user, get_auth_service
from database import get_session
from models import User, FoodItem
from services.auth_service import AuthenticationService

# Use in-memory SQLite for tests
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", 
        connect_args={"check_same_thread": False}, 
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        # Mock close to prevent app from closing the test session
        session.close = MagicMock()
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    
    # We might need to mock get_database if it's still used directly somewhere (it shouldn't be for SQLite)
    # But main.py uses 'create_db_and_tables' from database.py.
    # We should override 'database.get_session' used in dependencies.
    # Also need to patch AuthenticationService if needed, but let's try using real one with test DB.
    
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture(name="auth_service")
def auth_service_fixture(session):
    # Retrieve a service instance with the test session if possible, 
    # but AuthenticationService instantiates UserRepository internally.
    # UserRepository instantiates database connection internally?
    # We refactored UserRepository to use 'get_session' or similar?
    # Actually, UserRepository likely creates its own session or uses a global get_session.
    # We need to ensure repositories use the test session.
    # Dependencies in main.py use Depends(get_session) usually.
    # But currently repositories might be instantiation-based: `self.db = get_database()`.
    # Let's check `backend/repositories/base.py`.
    # If they use `get_session()` inside, overriding it in `app.dependency_overrides` might NOT affect 
    # manual instantiation `UserRepository()`.
    # We need to patch `repositories.base.get_session` or similar.
    pass

@pytest.fixture(autouse=True)
def patch_get_session(session):
    # Patch the get_session used by repositories. 
    # BaseRepository calls next(get_session()). 
    # So we need get_session() to return an iterator yielding the session.
    def mock_get_session():
        yield session
    
    with patch("repositories.base.get_session", side_effect=mock_get_session):
        yield

@pytest.fixture(name="test_user")
def test_user_fixture(session, client):
    # Create a user in the DB
    from services.auth_service import AuthenticationService
    auth_service = AuthenticationService() 
    # Note: AuthenticationService logic needs to use the session. 
    # If it uses UserRepository(), and UserRepository uses get_session(), the patch above handles it.
    
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword",
        "age": 30
    }
    
    # Use register_user to handle hashing
    user_id = auth_service.register_user(user_data, user_data["password"])
    
    user = session.get(User, user_id)
    return user

@pytest.fixture(name="auth_headers")
def auth_headers_fixture(test_user):
    from services.auth_service import AuthenticationService
    auth_service = AuthenticationService()
    token = auth_service.create_access_token(data={"sub": test_user.email})
    return {"Authorization": f"Bearer {token}"}

