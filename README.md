# Amauta.ai - El Google Flights de Educación en LatAm

Amauta.ai es una plataforma diseñada para centralizar y comparar ofertas educativas en Latinoamérica, comenzando por el mercado peruano.

## Sprint 1: Harvester Pilot (UTEC/UPC) - COMPLETED
- [x] Estructura base del proyecto.
- [x] Esquema inicial de PostgreSQL orientado a geolocalización.
- [x] Scripts de recolección de datos iniciales.
- [x] **8 programas de DATA capturados** (UTEC & UPC Pilot).

## Sprint 2: FastAPI Backend & Security Audit - COMPLETED
- [x] **Backend Core:** FastAPI application in `/api` with SQLAlchemy ORM.
- [x] **Secure API:** Implemented `GET /courses` with filtering (name, mode, max_price).
- [x] **Security Audit:** Standardized Pydantic validation and global exception handling (no error traces).
- [x] **Automated Testing:** 100% test coverage for API endpoints with Pytest (`tests/test_sprint2.py`).
- [x] **Frontend Init:** Next.js 14 configurado en `/web` con Tailwind CSS y Shadcn/UI.

## API Technical Documentation

### Base URL
`http://localhost:8000` (default for development)

### Endpoints

#### 1. Search Courses
`GET /courses`

Returns a list of courses with optional filters.

**Query Parameters:**
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `name` | string | Partial, case-insensitive match for course name. |
| `mode` | string | Filter by modality: `Presencial`, `Híbrido`, `Remoto`. |
| `max_price` | decimal | Maximum price in PEN. |

**Example Request:**
`GET /courses?name=Ciencia&mode=Remoto&max_price=1000`

**Example Response:**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "institution_id": "6eb31464-a690-4963-9562-b9116a49591e",
    "institution_name": "UPN",
    "name": "Ingeniería en Ciencia de Datos",
    "slug": "ingenieria-en-ciencia-de-datos",
    "price_pen": 0.0,
    "mode": "Híbrido",
    "address": "Sede Breña/Los Olivos, Lima",
    "duration": "10 ciclos",
    "url": "https://www.upn.edu.pe/...",
    "last_scraped_at": "2026-03-27T10:00:00Z",
    "created_at": "2026-03-27T10:00:00Z",
    "updated_at": "2026-03-27T10:00:00Z"
  }
]
```

### Security & Error Handling
- **SQL Injection Prevention:** All queries use SQLAlchemy ORM with parameterized inputs.
- **Data Validation:** Pydantic schemas enforce strict typing and constraints on all API inputs/outputs.
- **Error Privacy:** A global exception handler catches all unhandled exceptions and returns a generic 500 message, preventing leakage of sensitive system information or stack traces.

## Arquitectura de Base de Datos
Estado actual: Operativa en Docker con PostgreSQL 16.
- [x] **Instituciones:** UTEC y UPC inicializadas.
- [x] **Cursos:** 8 registros activos con metadata de modalidad y geolocalización.

### Esquema SQL (Sprint 1.1)
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table: institutions
CREATE TABLE institutions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    website_url TEXT,
    location_lat DECIMAL(10, 8),
    location_long DECIMAL(11, 8),
    address TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table: courses
CREATE TABLE courses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    institution_id UUID NOT NULL REFERENCES institutions(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255),
    price_pen DECIMAL(12, 2),
    mode VARCHAR(50),
    address TEXT,
    duration VARCHAR(100),
    url TEXT,
    last_scraped_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

---
*Documentación generada automáticamente por el servidor MCP de GitHub - Amauta.ai Architect*
