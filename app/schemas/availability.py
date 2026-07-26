from datetime import datetime
from pydantic import BaseModel, Field

class AvailabilityCreate(BaseModel):
    doctor_id: int
    start_time: datetime
    end_time: datetime
    consultation_duration: int = Field(gt=0)
    buffer_minutes: int = Field(default=0, ge=0)

class AvailabilityResponse(BaseModel):
    id: int
    doctor_id: int
    start_time: datetime
    end_time: datetime
    consultation_duration: int
    buffer_minutes: int

    model_config = {
        "from_attributes": True
    }