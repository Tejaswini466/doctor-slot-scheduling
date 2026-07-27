import pytest

def create_test_slot(client):
    response = client.post(
        "/availability/",
        json={
            "doctor_id": 1,
            "start_time": "2026-09-01T09:00:00Z",
            "end_time": "2026-09-01T10:00:00Z",
            "consultation_duration": 15,
            "buffer_minutes": 0,
        },
    )
    assert response.status_code == 200
    availability_id = response.json()["id"]
    slots = client.get("/slots/").json()
    new_slots = [
        slot for slot in slots
        if slot["availability_id"] == availability_id
    ]
    assert len(new_slots) > 0
    new_slots.sort(key=lambda x: x["id"], reverse=True)
    return new_slots[0]["id"]

def test_book_slot(client):
    slot_id = create_test_slot(client)

    response = client.post(
        "/booking/",
        json={
            "slot_id": slot_id,
            "patient_name": "Test User"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["slot_id"] == slot_id
    assert data["patient_name"] == "Test User"
    assert data["status"] == "confirmed"

def test_double_booking(client):
    slot_id = create_test_slot(client)
    first = client.post(
        "/booking/",
        json={
            "slot_id": slot_id,
            "patient_name": "Alice"
        },
    )
    assert first.status_code == 200
    second = client.post(
        "/booking/",
        json={
            "slot_id": slot_id,
            "patient_name": "Bob"
        },
    )
    assert second.status_code == 400
    assert second.json()["detail"] == "Slot is already booked."

def test_cancel_booking(client):
    slot_id = create_test_slot(client)
    booking = client.post(
        "/booking/",
        json={
            "slot_id": slot_id,
            "patient_name": "Cancel Test"
        },
    )
    assert booking.status_code == 200
    booking_id = booking.json()["id"]
    cancel = client.patch(f"/booking/{booking_id}/cancel")
    assert cancel.status_code == 200
    assert cancel.json()["status"] == "cancelled"