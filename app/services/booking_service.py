from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.booking import Booking
from app.models.slot import Slot
from app.schemas.booking import BookingCreate

def book_slot(
    db: Session,
    booking_data: BookingCreate,
):
    slot = (
        db.query(Slot)
        .filter(Slot.id == booking_data.slot_id)
        .with_for_update(nowait=True)  #don't touch until it's done. Row-level locking
        .first()
    )

    if slot is None:
        raise HTTPException(
            status_code=404,
            detail="Slot not found."
        )
    if slot.status != "available":
        raise HTTPException(
            status_code=400,
            detail="Slot is already booked."
        )
    booking = Booking(
        slot_id=booking_data.slot_id,
        patient_name=booking_data.patient_name,
    )
    slot.status = "booked"
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

def cancel_booking(
    db: Session,
    booking_id: int,
):
    booking = (
        db.query(Booking)
        .filter(Booking.id == booking_id)
        .first()
    )
    if booking is None:
        raise HTTPException(
            status_code=404,
            detail="Booking not found."
        )
    if booking.status == "cancelled":
        raise HTTPException(
            status_code=409,
            detail="Slot is already booked."
        )
    slot = booking.slot
    booking.status = "cancelled"
    slot.status = "available"
    db.commit()
    db.refresh(booking)
    return booking