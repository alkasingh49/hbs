# Hotel Booking Assignment Steps

This document maps the assignment requirements to the current project and the work done to complete each step.

## Step 1: Fix double booking logic

### What was done
- Added model-level overlap validation in `bookings/models.py`
- Added `Booking.save()` to call `full_clean()` before saving
- Updated `bookings/views.py` to use `transaction.atomic()` and `select_for_update()` on the room before saving
- Added a second overlap check inside the transaction

### Why it matters
- Prevents two users from booking the same room for overlapping dates
- Enforces validation both in the view and at the model layer

## Step 2: Write tests

### Added tests
- `bookings/tests.py`
  - validation tests for past dates, invalid ranges, overlapping bookings, coupon handling, and back-to-back booking
- `bookings/tests_concurrency.py`
  - concurrency test for PostgreSQL row locking and preventing double-booking
- `rooms/tests.py`
  - room search filters for room type, price range, availability, and booked dates
- `accounts/tests.py`
  - signup redirect and profile booking list tests

### Why it matters
- Ensures the booking and search logic behaves correctly
- Verifies the system is robust against invalid input and overlapping reservations

## Step 3: Move SQLite → PostgreSQL

### Current support
- `config/settings.py` already supports PostgreSQL through environment variables:
  - `DB_ENGINE`
  - `DB_NAME`
  - `DB_USER`
  - `DB_PASSWORD`
  - `DB_HOST`
  - `DB_PORT`

### Notes
- Default development remains SQLite for simplicity
- Use `.env.example` to configure PostgreSQL locally

## Step 4: Add Docker

### Added files
- `Dockerfile`
- `docker-compose.yml`
- `.dockerignore`

### What these do
- Build a Python/Django web container
- Run PostgreSQL in a separate container
- Link environment variables to the Django app

## Step 5: Add Ruff + pre-commit

### Added files
- `requirements-dev.txt`
- `.pre-commit-config.yaml`
- `.ruff.toml`

### What these do
- Enable automatic linting and formatting
- Enforce code quality before commits

## Step 6: README and documentation

### Added or updated
- `README.md`
- `ASSIGNMENT_STEPS.md`

### What these documents provide
- Quick setup instructions
- PostgreSQL and Docker usage
- Testing and development workflow
- Assignment completion details
