import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import MagicMock, patch
from uuid import uuid4
from datetime import datetime
from decimal import Decimal
from collections import namedtuple

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

def test_get_course_detail_success(client, mock_db):
    # Mock data
    mock_institution_id = uuid4()
    mock_course_id = uuid4()
    
    Row = namedtuple("Row", ["id", "institution_id", "name", "slug", "price_pen", "mode", "address", "duration", "url", "expected_monthly_salary", "last_scraped_at", "created_at", "updated_at", "institution_name", "location_lat", "location_long"])
    
    mock_row = Row(
        id=mock_course_id,
        institution_id=mock_institution_id,
        name="Test Course Detail",
        slug="test-course-detail",
        price_pen=Decimal("1000.00"),
        mode="Remoto",
        address="Test Address",
        duration="1 month",
        url="http://example.com",
        expected_monthly_salary=Decimal("2000.00"),
        last_scraped_at=datetime.now(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        institution_name="Test Institution",
        location_lat=Decimal("-12.1223"),
        location_long=Decimal("-77.0298")
    )

    mock_query = mock_db.query.return_value
    mock_join = mock_query.join.return_value
    mock_filter = mock_join.filter.return_value
    mock_filter.first.return_value = mock_row

    with patch("api.utils.get_client_coordinates", return_value=(-12.1223, -77.0298)):
        response = client.get("/courses/test-course-detail")
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Course Detail"
    assert data["roi_months"] == 0.5  # 1000 / 2000
    assert data["distance_km"] == 0.0

def test_get_course_detail_not_found(client, mock_db):
    mock_query = mock_db.query.return_value
    mock_join = mock_query.join.return_value
    mock_filter = mock_join.filter.return_value
    mock_filter.first.return_value = None

    response = client.get("/courses/non-existent")
    assert response.status_code == 404
    assert response.json()["detail"] == "Course not found"

def test_create_lead_success(client, mock_db):
    mock_course_id = uuid4()
    mock_course = models.Course(id=mock_course_id)
    
    mock_db.query.return_value.filter.return_value.first.return_value = mock_course
    
    # Mocking db.refresh to set id and created_at
    def mock_refresh(instance):
        instance.id = uuid4()
        instance.created_at = datetime.now()
    
    mock_db.refresh.side_effect = mock_refresh
    
    lead_data = {
        "course_id": str(mock_course_id),
        "name": "Juan Perez",
        "email": "juan@example.com",
        "phone": "987654321",
        "message": "Quiero info"
    }

    response = client.post("/leads", json=lead_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Juan Perez"
    assert "id" in data
    assert "created_at" in data
    assert mock_db.add.called
    assert mock_db.commit.called

def test_create_lead_course_not_found(client, mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    lead_data = {
        "course_id": str(uuid4()),
        "name": "Juan Perez",
        "email": "juan@example.com",
        "phone": "987654321"
    }

    response = client.post("/leads", json=lead_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Course not found"
