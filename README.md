# Workout Tracker API

A RESTful API for tracking workouts, exercises, and personal records. Built with FastAPI, SQLAlchemy, and JWT authentication.

## Features

- **Authentication** — register and log in with JWT tokens
- **Workout Management** — create, schedule, update, and delete workouts
- **Exercise Library** — seeded library of exercises with categories and muscle groups
- **Workout Templates** — save workout structures and spawn new workouts from them
- **Personal Records** — automatically tracked when a workout is completed
- **Reports** — summary stats over a configurable time period
- **Tests** — 27 passing tests with a dedicated test database

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM
- [SQLite](https://www.sqlite.org/) — database (swappable for PostgreSQL)
- [Pydantic](https://docs.pydantic.dev/) — data validation
- [python-jose](https://github.com/mpdavis/python-jose) — JWT tokens
- [passlib](https://passlib.readthedocs.io/) — password hashing
- [pytest](https://pytest.org/) — testing

## Project Structure

```
workout-tracker/
├── app/
│   ├── main.py                  # App entry point
│   ├── api/
│   │   └── routes/
│   │       ├── auth.py          # Register, login
│   │       ├── workouts.py      # Workout CRUD + exercise list
│   │       ├── templates.py     # Workout templates + spawn
│   │       ├── personal_records.py
│   │       └── reports.py
│   ├── core/
│   │   ├── config.py            # Settings from .env
│   │   ├── security.py          # JWT + password hashing
│   │   └── pr_checker.py        # Personal record logic
│   ├── db/
│   │   ├── base.py              # SQLAlchemy Base
│   │   ├── session.py           # Engine + session factory
│   │   └── seed.py              # Exercise seeder
│   ├── models/
│   │   ├── user.py
│   │   ├── workout.py           # Workout, WorkoutExercise, PersonalRecord, Templates
│   │   └── exercise.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── workout.py
│   │   ├── template.py
│   │   ├── exercise.py
│   │   └── personal_record.py
│   └── tests/
│       ├── conftest.py          # Fixtures + test DB setup
│       ├── test_auth.py
│       ├── test_workouts.py
│       ├── test_templates.py
│       └── test_reports.py
├── .env
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- pip

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/workout-tracker.git
cd workout-tracker
```

2. Create and activate a virtual environment:

```bash
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite:///./workout_tracker.db
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> For production, generate a secure secret key with:
> ```bash
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

5. Start the server:

```bash
uvicorn app.main:app --reload
```

The API will be running at `http://127.0.0.1:8000`.  
On first startup, the database is created and seeded with 10 exercises automatically.

## API Documentation

Interactive docs are available at:

- **Swagger UI** — `http://127.0.0.1:8000/docs`
- **ReDoc** — `http://127.0.0.1:8000/redoc`

## Endpoints

### Auth

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create a new account |
| POST | `/auth/login` | Log in and receive a JWT token |

### Workouts

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/workouts/` | Create a new workout |
| GET | `/workouts/` | List all workouts (filter by status) |
| GET | `/workouts/{id}` | Get a single workout |
| PATCH | `/workouts/{id}` | Update a workout |
| DELETE | `/workouts/{id}` | Delete a workout |
| GET | `/workouts/exercises/all` | List all available exercises |

### Templates

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/templates/` | Create a workout template |
| GET | `/templates/` | List all templates |
| GET | `/templates/{id}` | Get a single template |
| PATCH | `/templates/{id}` | Update a template |
| DELETE | `/templates/{id}` | Delete a template |
| POST | `/templates/{id}/spawn` | Create a workout from a template |

### Personal Records

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/personal-records/` | Get all personal records |
| GET | `/personal-records/exercise/{id}` | Get PRs for a specific exercise |

### Reports

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/reports/summary?days=30` | Workout summary for the last N days |

## Authentication

All endpoints except `/auth/register` and `/auth/login` require a Bearer token.

Include it in the `Authorization` header:

```
Authorization: Bearer <your_token>
```

## Example Usage

### 1. Register and log in

```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "ada", "email": "ada@example.com", "password": "password123"}'

# Log in
curl -X POST http://localhost:8000/auth/login \
  -d "username=ada&password=password123"
```

### 2. Create a workout

```bash
curl -X POST http://localhost:8000/workouts/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Chest Day",
    "scheduled_at": "2026-04-10T10:00:00",
    "exercises": [
      {"exercise_id": 1, "sets": 4, "reps": 8, "weight_kg": 80}
    ]
  }'
```

### 3. Mark it completed (triggers PR check)

```bash
curl -X PATCH http://localhost:8000/workouts/1 \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

### 4. Check your personal records

```bash
curl http://localhost:8000/personal-records/ \
  -H "Authorization: Bearer <token>"
```

## Running Tests

```bash
python -m pytest app/tests/ -v
```

Expected output:

```
app/tests/test_auth.py::test_register_success                    PASSED
app/tests/test_auth.py::test_register_duplicate_email            PASSED
app/tests/test_auth.py::test_login_success                       PASSED
...
27 passed, 0 warnings
```

## Database Schema

| Table | Description |
|-------|-------------|
| `users` | User accounts |
| `exercises` | Exercise library (seeded on startup) |
| `workouts` | User workouts with status and schedule |
| `workout_exercises` | Exercises within a workout (sets, reps, weight) |
| `workout_templates` | Reusable workout structures |
| `template_exercises` | Exercises within a template |
| `personal_records` | Best performance per exercise per user |

## License

MIT
