from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.booking import BookingCreate, BookingResponse
from app.services.booking_service import book_slot

router = APIRouter(
    prefix="/booking",
    tags=["Booking"],
)

@router.post(
    "/",
    response_model=BookingResponse,
)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
):
    return book_slot(db, booking)