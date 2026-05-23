# Hotel Booking — Assignment Guide (Beginner Friendly)

This guide explains what to do for each assignment step and which project files are relevant. Follow the order below — each section includes short commands and what to check.

---

## Quick setup (do this first)

1. Open a terminal and go to the project folder:

```bash
cd /home/alka.singh/Downloads/hbs-main
```

2. Activate the virtual environment:

```bash
source .venv/bin/activate
```

3. Install Python dependencies (if not already):

```bash
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

4. Run migrations and start server (SQLite default):

```bash
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/ in the browser.

---

## Overview of the assignment steps

The assignment contains these high-level tasks. Below each step you'll find which files implement the behavior and what to test.

### STEP 1 — Fix double booking logic

Goal: Prevent two users from booking the same room for overlapping dates.

Files to inspect and edit:
- `bookings/models.py` — model-level validation for overlaps and business rules (check_in/check_out). This ensures invalid bookings cannot be saved.
- `bookings/views.py` — booking creation flow. Use transactions (`transaction.atomic`) and `select_for_update()` to avoid race conditions.
- `bookings/forms.py` — user input validation for the booking form.
- `bookings/admin.py` — admin list to inspect bookings.

What to check:
- Create two overlapping bookings in the UI or via the shell — the second booking must fail with a validation message.
- Run unit tests for bookings:

```bash
python manage.py test bookings
```

Why these files:
- `models.py` enforces the invariant at the data layer (strongest guarantee).
- `views.py` handles concurrency protection when multiple requests run at the same time.
- `forms.py` prevents simple invalid input reaching the model.


### STEP 2 — Write tests

Files added/used for tests:
- `bookings/tests.py` — unit tests for booking validation and coupon handling.
- `bookings/tests_concurrency.py` — concurrency test that requires PostgreSQL (row locking). Skips on SQLite.
- `rooms/tests.py` — tests for the search/filter behaviour.
- `accounts/tests.py` — signup and profile tests.

How to run tests:

```bash
python manage.py test
```

Notes:
- Concurrency tests require PostgreSQL. Run them in a Docker-based Postgres environment (see STEP 4).


### STEP 3 — Move SQLite → PostgreSQL

Files and configuration:
- `config/settings.py` — database configuration supports environment-driven DB settings (`DB_ENGINE`, `DB_NAME`, etc.).
- `.env.example` — environment template for Postgres credentials.
- `scripts/migrate_postgres.sh` — helper to run migrations against Postgres.

How to try Postgres locally (Docker):

1. Copy `.env.example` to `.env` and customise credentials.
2. Start Docker services:

```bash
docker compose up --build -d
```

3. Run migrations:

```bash
./scripts/migrate_postgres.sh
```

4. Run tests against Postgres (ensure `DB_ENGINE` points to `django.db.backends.postgresql`).

Why:
- SQLite is simple for dev, but PostgreSQL supports row-level locking and is required for concurrency tests.


### STEP 4 — Add Docker

Files added:
- `Dockerfile` — builds the web container image.
- `docker-compose.yml` — runs `web` + `db` Postgres services.
- `.dockerignore` — ignore files for the build context.

Basic Docker flow:

```bash
# build & run
docker compose up --build -d
# run migrations
./scripts/migrate_postgres.sh
# view logs
docker compose logs -f web
```

Why:
- Docker provides an isolated environment with Postgres to reproduce production-like behaviour.


### STEP 5 — Add Ruff + pre-commit

Files and purpose:
- `requirements-dev.txt` — developer tooling packages (pre-commit, ruff).
- `.pre-commit-config.yaml` — pre-commit hooks configuration.
- `.ruff.toml` — Ruff configuration.

How to enable locally:

```bash
python -m pip install -r requirements-dev.txt
pre-commit install
pre-commit run --all-files
```

Why:
- Keeps code formatted and enforces basic lint rules automatically before commits.


### STEP 6 — README + docs for submission

Files:
- `README.md` — quick start and project overview (already updated).
- `ASSIGNMENT_STEPS.md` — short summary of the changes made for the assignment.
- `ASSIGNMENT_GUIDE.md` — (this file) in-depth beginner-friendly guide with commands and file mapping.

What to include for submission:
- A short explanation of each step and the files changed (see this document).
- Test results (output from `python manage.py test`).
- If you used Docker, include exact `.env` values you used (sanitise secrets).

---

## End-to-end flow (what happens when a user books a room)

1. Guest visits the site (`rooms/room_list`) — `rooms/views.py` reads available rooms and applies filters (`rooms/forms.py`). Template: `rooms/templates/rooms/room_list.html`.
2. Guest opens booking page (`bookings/views.book_room`) — `bookings/forms.py` validates dates and coupon.
3. On submit, `bookings/views.py` starts a DB transaction and locks the `Room` row with `select_for_update()` — this prevents concurrent writes.
4. The view re-checks for overlapping bookings (query in `bookings/views.py`) and then saves a new `Booking` record. `bookings/models.py` also validates overlaps in `clean()` before saving.
5. User is redirected to profile; profile shows bookings (`accounts/views.py` + `accounts/templates/registration/profile.html`).


## Helpful commands quick reference

Activate venv:

```bash
source .venv/bin/activate
```

Install deps:

```bash
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

Run tests:

```bash
python manage.py test
```

Run dev server (SQLite):

```bash
python manage.py runserver
```

Run with Docker/Postgres:

```bash
docker compose up --build -d
./scripts/migrate_postgres.sh
python manage.py test
```


## Troubleshooting tips (beginner-friendly)

- If `ImportError: Couldn't import Django` appears, ensure you activated the venv and installed dependencies.
- If tests that depend on row-level locking fail locally, run them with Postgres (Docker) — SQLite does not support the same locking semantics.
- If pre-commit prevents commit, run `pre-commit run --all-files` to see issues and auto-fix where possible.

---

If you want, I can now:
- Generate a concise submission-ready `README_SUBMISSION.md` summarising the assignment changes.
- Create small screenshots or sample curl commands to demonstrate booking flows.

Tell me which option you prefer next.
