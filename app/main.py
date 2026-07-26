from fastapi import FastAPI

app = FastAPI(
    title="Doctor Slot Scheduling API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "Doctor Slot Scheduling API is running!"}
