from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class Availability(Base):
    __tablename__ = "availability"
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(
        Integer,
        ForeignKey("doctor.id", ondelete="CASCADE"),
        nullable=False
    )
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    consultation_duration = Column(Integer, nullable=False)
    buffer_minutes = Column(Integer, default=0)

    doctor = relationship(
        "Doctor",
        back_populates="availabilities"
    )
    slots = relationship( #one availability many slots
        "Slot",
        back_populates="availability",
        cascade="all, delete-orphan"
    )