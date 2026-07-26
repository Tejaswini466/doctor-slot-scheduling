from sqlalchemy.orm import Session
from app.models.slot import Slot

def get_available_slots(db: Session):
    return (
        db.query(Slot)
        .filter(Slot.status == "available")
        .order_by(Slot.start_time)
        .all()
    )