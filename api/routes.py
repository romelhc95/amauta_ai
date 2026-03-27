from fastapi import APIRouter, Depends, Query, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal
from . import models, schemas, database, utils

router = APIRouter()

@router.get("/courses", response_model=List[schemas.CourseResponse])
async def get_courses(
    request: Request,
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
        models.Institution.name.label("institution_name"),
        models.Institution.location_lat,
        models.Institution.location_long
    ).join(models.Institution, models.Course.institution_id == models.Institution.id)

    if name:
        query = query.filter(models.Course.name.ilike(f"%{name}%"))
    
    if mode:
        query = query.filter(models.Course.mode == mode)
    
    if max_price is not None:
        query = query.filter(models.Course.price_pen <= max_price)

    results = query.all()

    # IP Geolocation Logic
    client_ip = request.client.host
    client_coords = await utils.get_client_coordinates(client_ip)

    processed_results = []
    for row in results:
        # Convert row to dict for manipulation
        if hasattr(row, "_fields"):
            course_dict = dict(zip(row._fields, row))
        else:
            # Handle cases where row might already be a dict (like in some tests)
            course_dict = dict(row)
        
        distance = None
        if client_coords and course_dict.get("location_lat") and course_dict.get("location_long"):
            inst_coords = (float(course_dict["location_lat"]), float(course_dict["location_long"]))
            distance = utils.calculate_distance(client_coords, inst_coords)
        
        course_dict["distance_km"] = distance
        processed_results.append(course_dict)

    # Sort by distance if available, otherwise just return results
    if client_coords:
        processed_results.sort(key=lambda x: x["distance_km"] if x["distance_km"] is not None else float('inf'))

    return processed_results
