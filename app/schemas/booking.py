from datetime import datetime
from pydantic import BaseModel

class BookingCreate(BaseModel):
    slot_id: int
    patient_name: str

class BookingResponse(BaseModel):
    id: int
    slot_id: int
    patient_name: str
    booked_at: datetime
    status: str
    model_config = {
        "from_attributes": True
    }