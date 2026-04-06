from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.db.seed import seed_exercises
from app.api.routes import (
    auth, workouts, reports, personal_records,
    templates, exercises, progress, body_measurements
)
import app.models.user      # noqa
import app.models.workout   # noqa
import app.models.exercise  # noqa

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_exercises()
    yield

app = FastAPI(
    title="Workout Tracker API",
    version="1.0.0",
    lifespan=lifespan,
    description="""
A REST API for tracking workouts, exercises, and personal records.

## Features
- **Authentication** — register and log in with JWT tokens
- **Workouts** — create, schedule, update, and delete workouts
- **Exercises** — global library plus custom user-created exercises
- **Templates** — save workout structures and spawn new workouts from them
- **Personal Records** — automatically tracked when a workout is completed
- **Progress** — strength curves, volume trends, and workout frequency
- **Body Measurements** — track weight, body fat, and measurements over time
- **Reports** — summary stats over a given time period

## Authentication
All endpoints except `/auth/register` and `/auth/login` require a Bearer token.
After logging in, click the **Authorize** button and paste your token.
    """,
    contact={"name": "Workout Tracker"},
    license_info={"name": "MIT"},
)

app.include_router(auth.router)
app.include_router(workouts.router)
app.include_router(exercises.router)
app.include_router(templates.router)
app.include_router(personal_records.router)
app.include_router(reports.router)
app.include_router(progress.router)
app.include_router(body_measurements.router)

@app.get("/", tags=["health"])
def root():
    return {"status": "ok", "message": "Workout Tracker API"}