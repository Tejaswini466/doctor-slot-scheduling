from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class Doctor(Base):
    __tablename__ = "doctor"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    #one doc has many availabilities and slots 
    availabilities = relationship(
        "Availability",
        back_populates="doctor",
        cascade="all, delete-orphan"
    )
    slots = relationship(
        "Slot",
        back_populates="doctor",
        cascade="all, delete-orphan"
    )