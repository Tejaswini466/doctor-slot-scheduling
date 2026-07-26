from fastapi import FastAPI
from sqlalchemy import text
from app.db.database import Base, engine
from app.models import Doctor, Availability, Slot, Booking
from app.db.database import SessionLocal
from app.api.availability import router as availability_router
from app.models.doctor import Doctor
from app.db.database import SessionLocal
from app.api.slot import router as slot_router

Base.metadata.create_all(bind=engine)
def seed_doctor():
    db = SessionLocal()
    if db.query(Doctor).count() == 0:
        doctor = Doctor(name="Dr. Smith")
        db.add(doctor)
        db.commit()
    db.close()

seed_doctor()
app = FastAPI(
    title="Doctor Slot Scheduling API",
    version="1.0.0",
)
app.include_router(availability_router)
app.include_router(slot_router)

@app.get("/")
def home():
    return {"message": "Doctor Slot Scheduling API is running!"}

@app.get("/db-test")
def db_test():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"message": "Database connection successful!"}
    finally:
        db.close()