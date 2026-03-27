from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from .routes import router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Amauta.ai API",
    description="API for managing courses and institutions",
    version="1.0.0"
)

# Standard error handler to avoid exposing internal traces
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred. Please try again later."}
    )

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Amauta.ai API"}
