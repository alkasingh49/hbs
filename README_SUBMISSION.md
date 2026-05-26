# Submission Notes — Hotel Booking System

This file summarises how to run and validate the project for submission.

## What I implemented
- Booking engine with double-booking prevention (model + view + form validation).
- Unit tests (bookings + rooms). Concurrency test included (requires PostgreSQL).
- Docker + docker-compose configuration for running Postgres locally.
- Pre-commit hooks and `ruff` configuration; lint fixes applied.
- Room manager UI for staff (create/edit rooms).
- Environment-driven settings to support switching between SQLite (dev) and Postgres (production).
- Documentation: `ASSIGNMENT_GUIDE.md` and `ASSIGNMENT_STEPS.md`.

## How to run locally (SQLite quick run)

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
python -m pip install -r requirements.txt
python -m pip install -r requirements-dev.txt
```

3. Apply migrations and run the server:

```bash
python manage.py migrate
python manage.py runserver
```

4. Run tests:

```bash
python manage.py test
```

## How to run with Docker + Postgres (recommended for concurrency tests)

1. Copy `.env.example` to `.env` and set Postgres values.
2. Start the services:

```bash
docker compose up --build -d
```

3. Run migrations against Postgres:

```bash
./scripts/migrate_postgres.sh
```

4. Run tests (they will run against Postgres if `DATABASE_URL` or DB env vars point to the container):

```bash
python manage.py test
```

## Notes
- Concurrency locking tests require PostgreSQL; SQLite cannot reproduce row-level locking semantics.
- `config/settings.py` now reads secrets from environment variables; set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, and DB env vars for production runs.

---

If you want, I can now:
- Attempt Docker installation steps on this machine (needs sudo privileges).
- Run the Postgres-based tests on your machine if you start Docker, or guide you through it step-by-step.

Tell me which you prefer.
