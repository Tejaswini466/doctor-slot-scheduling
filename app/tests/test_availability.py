def test_create_availability(client):
    response = client.post(
        "/availability/",
        json={
            "doctor_id": 1,
            "start_time": "2026-08-01T09:00:00Z",
            "end_time": "2026-08-01T10:00:00Z",
            "consultation_duration": 15,
            "buffer_minutes": 0
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["doctor_id"] == 1
    assert data["consultation_duration"] == 15

def test_slots_generated(client):
    response = client.get("/slots/")
    assert response.status_code == 200
    slots = response.json()
    assert len(slots) > 0