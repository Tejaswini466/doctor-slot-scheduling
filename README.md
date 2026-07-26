# Doctor Slot Scheduling API

A backend system for managing doctor availability, automatically generating appointment slots, and enabling concurrency-safe slot booking. The project is built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy**, with a focus on data integrity, transactional consistency, and scalable backend design.

---

# Features

* Create doctor availability windows.
* Automatically generate appointment slots based on:

  * Consultation duration
  * Buffer time between appointments
* View all available appointment slots.
* Book an appointment slot.
* Prevent double booking using PostgreSQL row-level locking.
* Cancel bookings and automatically release slots.
* Safely update doctor availability while protecting existing bookings.
* RESTful API documented with Swagger UI.
* Integration tests using Pytest.

---

# Tech Stack

| Component         | Technology        |
| ----------------- | ----------------- |
| Backend Framework | FastAPI           |
| Language          | Python 3.10+      |
| Database          | PostgreSQL        |
| ORM               | SQLAlchemy        |
| Validation        | Pydantic          |
| API Documentation | Swagger (OpenAPI) |
| Testing           | Pytest            |
| Version Control   | Git & GitHub      |

---

# Project Structure

```text
doctor-slot-scheduling/
│
├── app/
│   ├── api/
│   │   ├── availability.py
│   │   ├── booking.py
│   │   └── slot.py
│   │
│   ├── db/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── doctor.py
│   │   ├── availability.py
│   │   ├── slot.py
│   │   └── booking.py
│   │
│   ├── schemas/
│   │   ├── availability.py
│   │   ├── booking.py
│   │   └── slot.py
│   │
│   ├── services/
│   │   ├── availability_service.py
│   │   ├── booking_service.py
│   │   └── slot_service.py
│   │
│   └── main.py
│
├── tests/
│   ├── conftest.py
│   ├── test_availability.py
│   └── test_booking.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# System Architecture

```text
                Client
                   │
             REST API (FastAPI)
                   │
        ┌──────────┴──────────┐
        │                     │
 Availability Service    Booking Service
        │                     │
        └──────────┬──────────┘
                   │
            SQLAlchemy ORM
                   │
             PostgreSQL
```

---

# Database Schema

## Doctor

| Field | Type    |
| ----- | ------- |
| id    | Integer |
| name  | String  |

---

## Availability

| Field                 | Type        |
| --------------------- | ----------- |
| id                    | Integer     |
| doctor_id             | Foreign Key |
| start_time            | Timestamp   |
| end_time              | Timestamp   |
| consultation_duration | Integer     |
| buffer_minutes        | Integer     |

---

## Slot

| Field           | Type               |
| --------------- | ------------------ |
| id              | Integer            |
| availability_id | Foreign Key        |
| doctor_id       | Foreign Key        |
| start_time      | Timestamp          |
| end_time        | Timestamp          |
| status          | available / booked |

---

## Booking

| Field        | Type                  |
| ------------ | --------------------- |
| id           | Integer               |
| slot_id      | Foreign Key (Unique)  |
| patient_name | String                |
| booked_at    | Timestamp             |
| status       | confirmed / cancelled |

---

# API Endpoints

## Create Availability

**POST**

```http
/availability/
```

Creates a doctor's availability and automatically generates appointment slots.

---

## Update Availability

**PATCH**

```http
/availability/{availability_id}
```

Updates availability only if none of its generated slots have already been booked.

Returns **409 Conflict** if booked slots exist.

---

## Get Available Slots

**GET**

```http
/slots/
```

Returns only slots whose status is **available**.

---

## Book Appointment

**POST**

```http
/booking/
```

Books an available appointment slot.

Returns **409 Conflict** if the slot has already been booked.

---

## Cancel Booking

**PATCH**

```http
/booking/{booking_id}/cancel
```

Cancels a booking and marks the associated slot as available again.

---

# Design Decisions

## Service Layer

Business logic is separated from API routes.

* API layer handles HTTP requests and responses.
* Service layer contains scheduling and booking logic.
* Models represent database entities.
* Schemas handle validation and serialization.

This separation improves readability and maintainability.

---

## Automatic Slot Generation

When availability is created:

1. Availability is stored.
2. Appointment slots are generated automatically.
3. All slots are persisted within the same database transaction.

This removes manual slot creation and keeps scheduling consistent.

---

## Transaction Management

Slot generation uses SQLAlchemy's `flush()` before the final `commit()`.

This ensures:

* Availability and generated slots are committed atomically.
* Partial data is never stored if slot generation fails.

---

# Concurrency Handling

The booking workflow is designed to prevent race conditions and duplicate bookings.

The implementation uses three layers of protection:

### 1. PostgreSQL Row-Level Locking

```python
.with_for_update(nowait=True)
```

The slot row is locked before checking its status.

If another transaction is already booking the same slot, PostgreSQL prevents simultaneous modifications.

---

### 2. Business Validation

Before creating a booking, the application verifies:

```text
Slot status == "available"
```

If not, the request returns a conflict response.

---

### 3. Database Constraint

The Booking table enforces a unique constraint on `slot_id`.

Even in unexpected situations, the database prevents duplicate bookings.

---

# Availability Update Strategy

Updating a doctor's availability after bookings already exist can compromise data integrity.

Instead of deleting booked slots or moving appointments automatically, the system rejects such updates.

Response:

```http
409 Conflict
```

This preserves:

* Existing appointments
* Audit history
* Data consistency

---

# Booking Cancellation Strategy

Bookings are **not deleted**.

Instead:

```text
confirmed
      ↓
cancelled
```

The associated slot becomes available again.

Advantages:

* Preserves booking history
* Supports auditing
* Avoids accidental data loss

---

# Testing

The project includes integration tests covering the complete scheduling workflow.

Tests include:

* Availability creation
* Automatic slot generation
* Successful booking
* Double booking prevention
* Booking cancellation

Run all tests:

```bash
pytest
```

---

# Assumptions

* A doctor already exists before creating availability.
* Appointment durations are expressed in minutes.
* Appointment slots cannot overlap.
* One booking corresponds to one slot.
* Cancelled bookings remain stored for audit purposes.
* Availability cannot be modified if booked slots exist.

---

# Trade-offs

Due to assignment scope and timeline:

* Authentication and authorization were not implemented.
* Notification services were not included.
* Multi-doctor scheduling conflicts were out of scope.
* Redis reservation holds were intentionally omitted.
* Tests use the development database rather than a dedicated test database.

---

# Future Improvements

* JWT-based authentication
* Role-based access control
* Redis reservation/hold mechanism
* Dedicated test database
* Docker containerization
* CI/CD pipeline using GitHub Actions
* Load testing using Locust
* Doctor and Patient CRUD APIs
* Pagination and filtering for slot listings
* Appointment reminders and notifications

---

# Setup Instructions

## Clone Repository

```bash
git clone <repository-url>
cd doctor-slot-scheduling
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure PostgreSQL

Create a PostgreSQL database and update the connection string inside:

```text
app/db/database.py
```

---

## Run the Application

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---
