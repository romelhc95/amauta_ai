from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional
from decimal import Decimal

class InstitutionBase(BaseModel):
    name: str

class InstitutionResponse(InstitutionBase):
    model_config = ConfigDict(from_attributes=True)

class CourseBase(BaseModel):
    name: str
    slug: Optional[str] = None
    price_pen: Optional[Decimal] = None
    mode: Optional[str] = None
    address: Optional[str] = None
    duration: Optional[str] = None
    url: Optional[str] = None

class CourseResponse(CourseBase):
    id: UUID
    institution_id: UUID
    institution_name: str
    last_scraped_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    distance_km: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)
