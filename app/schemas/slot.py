from datetime import datetime
from pydantic import BaseModel

class SlotResponse(BaseModel):
    id: int
    doctor_id: int
    availability_id: int
    start_time: datetime
    end_time: datetime
    status: str
    model_config = {
        "from_attributes": True
    }