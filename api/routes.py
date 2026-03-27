from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal
from . import models, schemas, database

router = APIRouter()

@router.get("/courses", response_model=List[schemas.CourseResponse])
def get_courses(
    name: Optional[str] = Query(None, description="Case-insensitive search by name"),
    mode: Optional[str] = Query(None, description="Filter by modality (Presencial, Híbrido, Remoto)"),
    max_price: Optional[Decimal] = Query(None, description="Maximum price in PEN"),
    db: Session = Depends(database.get_db)
):
    query = db.query(
        models.Course.id,
        models.Course.institution_id,
        models.Course.name,
        models.Course.slug,
        models.Course.price_pen,
        models.Course.mode,
        models.Course.address,
        models.Course.duration,
        models.Course.url,
        models.Course.last_scraped_at,
        models.Course.created_at,
        models.Course.updated_at,
        models.Institution.name.label("institution_name")
    ).join(models.Institution, models.Course.institution_id == models.Institution.id)

    if name:
        query = query.filter(models.Course.name.ilike(f"%{name}%"))
    
    if mode:
        query = query.filter(models.Course.mode == mode)
    
    if max_price is not None:
        query = query.filter(models.Course.price_pen <= max_price)

    results = query.all()
    return results
