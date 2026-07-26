from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.availability import (
    AvailabilityCreate,
    AvailabilityResponse,
)
from app.services.availability_service import create_availability

router = APIRouter(
    prefix="/availability",
    tags=["Availability"],
)

@router.post(
    "/",
    response_model=AvailabilityResponse,
)
def create_availability_endpoint(
    availability: AvailabilityCreate,
    db: Session = Depends(get_db),):
    return create_availability(db, availability)