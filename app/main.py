from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import SessionLocal

app = FastAPI(
    title="Doctor Slot Scheduling API",
    version="1.0.0",
)

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