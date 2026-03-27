import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import MagicMock
from uuid import uuid4
from decimal import Decimal
from datetime import datetime

from api.main import app
from api.database import get_db
from api import schemas

# Mock courses based on scripts/discover_courses.py
MOCK_COURSES = [
    {
        "id": uuid4(),
        "institution_id": uuid4(),
        "institution_name": "UPN",
        "name": "Ingeniería en Ciencia de Datos",
        "slug": "ingenieria-en-ciencia-de-datos",
        "price_pen": Decimal("0.00"),
        "mode": "Híbrido",
        "address": "Sede Breña/Los Olivos, Lima",
        "duration": "10 ciclos",
        "url": "https://www.upn.edu.pe/carreras/ingenieria-en-ciencia-de-datos",
        "last_scraped_at": datetime.now(),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": uuid4(),
        "institution_id": uuid4(),
        "institution_name": "USMP",
        "name": "Ingeniería de Ciencia de Datos",
        "slug": "ingenieria-de-ciencia-de-datos",
        "price_pen": Decimal("0.00"),
        "mode": "Presencial",
        "address": "Facultad de Ingeniería y Arquitectura, La Molina",
        "duration": "10 ciclos",
        "url": "https://usmp.edu.pe/ingenieria-de-ciencia-de-datos/",
        "last_scraped_at": datetime.now(),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": uuid4(),
        "institution_id": uuid4(),
        "institution_name": "Senati",
        "name": "Ingeniería de Ciencia de Datos e Inteligencia Artificial",
        "slug": "ingenieria-de-ciencia-de-datos-e-inteligencia-artificial",
        "price_pen": Decimal("0.00"),
        "mode": "Presencial",
        "address": "Sede Independencia, Lima",
        "duration": "6 ciclos",
        "url": "https://www.senati.edu.pe/especialidades/tecnologias-de-la-informacion/ingenieria-de-ciencia-de-datos-e-inteligencia-artificial",
        "last_scraped_at": datetime.now(),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": uuid4(),
        "institution_id": uuid4(),
        "institution_name": "UNI",
        "name": "Maestría en Data Science",
        "slug": "maestria-en-data-science",
        "price_pen": Decimal("0.00"),
        "mode": "Híbrido",
        "address": "FIEECS, Rímac",
        "duration": "4 ciclos",
        "url": "https://www.uni.edu.pe/posgrado/",
        "last_scraped_at": datetime.now(),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": uuid4(),
        "institution_id": uuid4(),
        "institution_name": "ESAN",
        "name": "Maestría en Data Analytics & AI",
        "slug": "maestria-en-data-analytics-ai",
        "price_pen": Decimal("0.00"),
        "mode": "Híbrido",
        "address": "Santiago de Surco, Lima",
        "duration": "24 meses",
        "url": "https://www.esan.edu.pe/maestrias/data-analytics-artificial-intelligence/",
        "last_scraped_at": datetime.now(),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": uuid4(),
        "institution_id": uuid4(),
        "institution_name": "ULima",
        "name": "Maestría en Ciencia de Datos para los Negocios",
        "slug": "maestria-en-ciencia-de-datos-para-los-negocios",
        "price_pen": Decimal("0.00"),
        "mode": "Híbrido",
        "address": "Santiago de Surco, Lima",
        "duration": "2 años",
        "url": "https://www.ulima.edu.pe/posgrado/maestrias/ciencia-de-datos-para-los-negocios",
        "last_scraped_at": datetime.now(),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": uuid4(),
        "institution_id": uuid4(),
        "institution_name": "Científica",
        "name": "Ingeniería en Inteligencia Artificial y Ciencia de Datos",
        "slug": "ingenieria-en-inteligencia-artificial-y-ciencia-de-datos",
        "price_pen": Decimal("0.00"),
        "mode": "Presencial",
        "address": "Sede Villa, Chorrillos",
        "duration": "10 ciclos",
        "url": "https://cientifica.edu.pe/carreras/ingenieria-en-inteligencia-artificial-y-ciencia-de-datos",
        "last_scraped_at": datetime.now(),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    },
    {
        "id": uuid4(),
        "institution_id": uuid4(),
        "institution_name": "DSRP",
        "name": "Programa especializado en Data Engineering",
        "slug": "programa-especializado-en-data-engineering",
        "price_pen": Decimal("0.00"),
        "mode": "Remoto",
        "address": "Online",
        "duration": "6 meses",
        "url": "https://datascience.pe/especializacion-data-engineering/",
        "last_scraped_at": datetime.now(),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
]

@pytest.fixture
def mock_db():
    mock = MagicMock(spec=Session)
    yield mock

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

def test_get_courses_count(client, mock_db):
    """Verify that GET /courses returns 8 courses"""
    mock_query = mock_db.query.return_value
    mock_join = mock_query.join.return_value
    mock_join.all.return_value = MOCK_COURSES

    response = client.get("/courses")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 8
    # Validate each item with Pydantic
    for item in data:
        schemas.CourseResponse(**item)

def test_get_courses_filter_name_success(client, mock_db):
    """Verify filtering by name works"""
    mock_query = mock_db.query.return_value
    mock_join = mock_query.join.return_value
    
    # Filter for "Maestría"
    filtered_courses = [c for c in MOCK_COURSES if "Maestría" in c["name"]]
    mock_join.filter.return_value.all.return_value = filtered_courses

    response = client.get("/courses?name=Maestría")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    for item in data:
        assert "Maestría" in item["name"]

def test_get_courses_filter_mode_success(client, mock_db):
    """Verify filtering by mode works"""
    mock_query = mock_db.query.return_value
    mock_join = mock_query.join.return_value
    
    # Filter for "Remoto"
    filtered_courses = [c for c in MOCK_COURSES if c["mode"] == "Remoto"]
    mock_join.filter.return_value.all.return_value = filtered_courses

    response = client.get("/courses?mode=Remoto")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["mode"] == "Remoto"

def test_get_courses_filter_price_success(client, mock_db):
    """Verify filtering by max_price works"""
    mock_query = mock_db.query.return_value
    mock_join = mock_query.join.return_value
    
    # Filter for max_price=500 (all current mock courses are 0.00)
    filtered_courses = [c for c in MOCK_COURSES if c["price_pen"] <= Decimal("500.00")]
    mock_join.filter.return_value.all.return_value = filtered_courses

    response = client.get("/courses?max_price=500")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 8

def test_security_error_handling(client, mock_db):
    """Verify internal errors are suppressed"""
    mock_db.query.side_effect = Exception("SENSITIVE_DB_ERROR: password=123")

    response = client.get("/courses")
    assert response.status_code == 500
    assert response.json() == {"detail": "An internal server error occurred. Please try again later."}
    assert "SENSITIVE_DB_ERROR" not in response.text
