from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Slot(Base):
    __tablename__ = "slot"
    id = Column(Integer, primary_key=True, index=True)
    availability_id = Column(
        Integer,
        ForeignKey("availability.id", ondelete="CASCADE"),
        nullable=False
    )
    doctor_id = Column(
        Integer,
        ForeignKey("doctor.id", ondelete="CASCADE"),
        nullable=False
    )

    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(20), default="available", nullable=False)

    availability = relationship(
        "Availability",
        back_populates="slots"
    )
    doctor = relationship(
        "Doctor",
        back_populates="slots"
    )
    booking = relationship(  #one-to-one
        "Booking",
        back_populates="slot",
        uselist=False,
        cascade="all, delete-orphan"
    )