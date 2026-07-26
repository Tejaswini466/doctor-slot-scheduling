from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Booking(Base):
    __tablename__ = "booking"
    id = Column(Integer, primary_key=True, index=True)
    slot_id = Column(
        Integer,
        ForeignKey("slot.id", ondelete="CASCADE"),
        unique=True,  #allowing only 1 person
        nullable=False
    )

    patient_name = Column(String(100), nullable=False)
    booked_at = Column(
        DateTime(timezone=True),
        server_default=func.now() #automatic
    )

    status = Column(String(20), default="confirmed", nullable=False)
    slot = relationship(
        "Slot",
        back_populates="booking"
    )