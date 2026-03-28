# Yachachiy.ai - El "Google Flights" de la Educación en Latinoamérica

Yachachiy.ai es una plataforma diseñada para centralizar, comparar y optimizar la búsqueda de ofertas educativas en Latinoamérica, comenzando con un enfoque estratégico en el mercado peruano.

## 🚀 Fases del Proyecto (Completadas)
- **Fase 1: Recolección Piloto**: Extracción de datos de universidades principales (UTEC/UPC).
- **Fase 2: API & Search UI**: Desarrollo del backend FastAPI y buscador principal.
- **Fase 3: Detalle & Leads**: Captura de interesados y páginas de detalle.
- **Fase 4: ROI Académico**: Cálculo inteligente del retorno de inversión.
- **Fase 5: Comparador & Mobile**: Herramienta de comparación y diseño responsivo.

## 🛠️ Cómo visualizar e interactuar con Yachachiy.ai

### 1. Requisitos
- Python 3.10+
- Node.js 18+
- SQLite (integrado)

### 2. Ejecución Local
*   **Backend (Puerto 8000):**
    ```powershell
    uvicorn api.main:app --reload
    ```
*   **Frontend (Puerto 3000):**
    ```powershell
    cd web; npm run dev
    ```

## 🐞 Remediación de Bugs
A continuación, se listan los errores críticos solucionados durante el desarrollo:

| Fecha | Error | Tipo | Descripción de la Solución |
| :--- | :--- | :--- | :--- |
| 28/03/2026 | `ReferenceError: ExternalLink is not defined` | Runtime | Se agregó la importación faltante de `ExternalLink` desde `lucide-react` en la página de comparación. |
| 28/03/2026 | `asChild prop on a DOM element` | React Console | El componente `@base-ui/react/button` no soporta `asChild`. Se refactorizó para usar clases de Tailwind directas sobre etiquetas `<a>`. |
| 28/03/2026 | `OperationalError: could not translate host name "db"` | Database | Se migró la arquitectura de PostgreSQL (Docker) a **SQLite** para facilitar la exploración local sin dependencias. |
| 28/03/2026 | `UnicodeDecodeError` en `.env` | Environment | Se corrigió la codificación del archivo `.env` creado por PowerShell a UTF-8 BOM. |

---
*Yachachiy.ai - Democratizando el acceso a la información educativa en LatAm.*
