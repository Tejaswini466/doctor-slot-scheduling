from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.availability import (
    AvailabilityCreate,
    AvailabilityResponse,
)
from app.services.availability_service import create_availability
from app.services.availability_service import (
    create_availability,
    update_availability,
)
from app.schemas.availability import AvailabilityUpdate

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

@router.patch(
    "/{availability_id}",
    response_model=AvailabilityResponse,
)
def update_availability_endpoint(
    availability_id: int,
    availability: AvailabilityUpdate,
    db: Session = Depends(get_db),
):
    return update_availability(
        db,
        availability_id,
        availability,
    )