def get_available_slot(client):
    response = client.get("/slots/")
    assert response.status_code == 200
    slots = response.json()
    assert len(slots) > 0
    return slots[0]["id"]

def test_book_slot(client):
    slot_id = get_available_slot(client)
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
    slot_id = get_available_slot(client)
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
    slot_id = get_available_slot(client)
    booking = client.post(
        "/booking/",
        json={
            "slot_id": slot_id,
            "patient_name": "Cancel Test"
        },
    )
    assert booking.status_code == 200
    booking_id = booking.json()["id"]
    cancel = client.patch(
        f"/booking/{booking_id}/cancel"
    )
    assert cancel.status_code == 200
    assert cancel.json()["status"] == "cancelled"