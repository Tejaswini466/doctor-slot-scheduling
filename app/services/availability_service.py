from datetime import timedelta
from sqlalchemy.orm import Session
from app.models.availability import Availability
from app.models.slot import Slot
from app.schemas.availability import AvailabilityCreate

def generate_slots(
    start_time,
    end_time,
    consultation_duration,
    buffer_minutes,
):
    slots=[]
    current=start_time
    while current+timedelta(minutes=consultation_duration) <= end_time:
        slot_end = current+timedelta(minutes=consultation_duration)
        slots.append((current,slot_end))
        current=slot_end+timedelta(minutes=buffer_minutes)
    return slots

def create_availability(
    db: Session,
    availability_data: AvailabilityCreate,
):
    availability = Availability(**availability_data.model_dump())
    db.add(availability)
    db.commit()
    db.refresh(availability)

    generated_slots = generate_slots(
        availability.start_time,
        availability.end_time,
        availability.consultation_duration,
        availability.buffer_minutes,
    )
    for start,end in generated_slots:
        slot = Slot(
            availability_id=availability.id,
            doctor_id=availability.doctor_id,
            start_time=start,
            end_time=end,
            status="available",
        )
        db.add(slot)
    db.commit()

    return availability