import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import MagicMock, patch
from uuid import uuid4
from datetime import datetime
from decimal import Decimal

from api.main import app
from api.database import get_db
from api import models, schemas

# Mock database session
@pytest.fixture
def mock_db():
    mock = MagicMock(spec=Session)
    yield mock

# Override get_db dependency
@pytest.fixture
def client(mock_db):
    def override_get_db():
        try:
            yield mock_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Amauta.ai API"}

def test_get_courses_success(client, mock_db):
    # Mock data
    mock_institution_id = uuid4()
    mock_course_id = uuid4()
    mock_course = MagicMock()
    mock_course.id = mock_course_id
    mock_course.institution_id = mock_institution_id
    mock_course.name = "Test Course"
    mock_course.slug = "test-course"
    mock_course.price_pen = Decimal("100.00")
    mock_course.mode = "Remoto"
    mock_course.address = None
    mock_course.duration = "1 month"
    mock_course.url = "http://example.com"
    mock_course.last_scraped_at = datetime.now()
    mock_course.created_at = datetime.now()
    mock_course.updated_at = datetime.now()
    mock_course.institution_name = "Test Institution"

    # Mocking the chain: db.query(...).join(...).filter(...).all()
    mock_query = mock_db.query.return_value
    mock_join = mock_query.join.return_value
    mock_join.all.return_value = [mock_course]

    response = client.get("/courses")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Course"
    assert data[0]["institution_name"] == "Test Institution"
    # Validate against schema (pydantic will raise error if it doesn't match)
    schemas.CourseResponse(**data[0])

def test_get_courses_filter_name(client, mock_db):
    mock_query = mock_db.query.return_value
    mock_join = mock_query.join.return_value
    mock_filter = mock_join.filter.return_value
    mock_filter.all.return_value = []

    response = client.get("/courses?name=Python")
    
    assert response.status_code == 200
    # Verify that filter was called
    assert mock_join.filter.called

def test_get_courses_filter_mode(client, mock_db):
    mock_query = mock_db.query.return_value
    mock_join = mock_query.join.return_value
    mock_filter = mock_join.filter.return_value
    mock_filter.all.return_value = []

    response = client.get("/courses?mode=Remoto")
    
    assert response.status_code == 200
    assert mock_join.filter.called

def test_get_courses_filter_price(client, mock_db):
    mock_query = mock_db.query.return_value
    mock_join = mock_query.join.return_value
    mock_filter = mock_join.filter.return_value
    mock_filter.all.return_value = []

    response = client.get("/courses?max_price=500")
    
    assert response.status_code == 200
    assert mock_join.filter.called

def test_global_exception_handler(client, mock_db):
    # Simulate a database error
    mock_db.query.side_effect = Exception("Database connection failed")

    response = client.get("/courses")
    
    assert response.status_code == 500
    assert response.json() == {"detail": "An internal server error occurred. Please try again later."}
