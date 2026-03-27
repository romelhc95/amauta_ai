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
- [x] **Automated Testing:** 100% test coverage for API endpoints with Pytest.
- [x] **Frontend Init:** Next.js 14 configurado en `/web` con Tailwind CSS y Shadcn/UI.
- [ ] Implementación de la UI inspirada en Google Flights.

## Estructura de la API
La API se encuentra en el directorio `/api` y utiliza FastAPI para exponer los datos de PostgreSQL.

### Endpoints
- `GET /courses`: Lista todos los cursos disponibles.
  - **Filtros:**
    - `name`: Búsqueda parcial por nombre (case-insensitive).
    - `mode`: Filtrar por modalidad (`Presencial`, `Híbrido`, `Remoto`).
    - `max_price`: Filtrar por precio máximo en PEN.

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
