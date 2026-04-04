from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta
from app.db.session import get_db
from app.models.workout import BodyMeasurement
from app.models.user import User
from app.schemas.body_measurement import (
    BodyMeasurementCreate,
    BodyMeasurementUpdate,
    BodyMeasurementOut,
)
from app.core.security import get_current_user
from app.core.pagination import Pagination

router = APIRouter(prefix="/body", tags=["body measurements"])


@router.post(
    "/",
    response_model=BodyMeasurementOut,
    status_code=201,
    summary="Log a body measurement",
    response_description="The saved measurement entry",
)
def log_measurement(
    payload: BodyMeasurementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Log a body measurement entry. All fields are optional — only log
    what you actually measured. You can backfill old entries by
    providing a custom **logged_at** date.
    """
    entry = BodyMeasurement(
        user_id=current_user.id,
        logged_at=payload.logged_at or datetime.utcnow(),
        weight_kg=payload.weight_kg,
        body_fat_pct=payload.body_fat_pct,
        chest_cm=payload.chest_cm,
        waist_cm=payload.waist_cm,
        hips_cm=payload.hips_cm,
        arms_cm=payload.arms_cm,
        legs_cm=payload.legs_cm,
        notes=payload.notes,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/", response_model=List[BodyMeasurementOut])
def list_measurements(
    days:       Optional[int] = None,
    pagination: Pagination = Depends(Pagination),
    db:         Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(BodyMeasurement).filter(
        BodyMeasurement.user_id == current_user.id
    )
    if days:
        since = datetime.utcnow() - timedelta(days=days)
        query = query.filter(BodyMeasurement.logged_at >= since)
    return query.order_by(BodyMeasurement.logged_at).offset(pagination.skip).limit(pagination.limit).all()


@router.get(
    "/latest",
    response_model=BodyMeasurementOut,
    summary="Get the most recent measurement",
    responses={404: {"description": "No measurements logged yet"}},
)
def latest_measurement(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns the single most recent body measurement entry.
    Useful for displaying current stats on a profile or dashboard screen.
    """
    entry = (
        db.query(BodyMeasurement)
        .filter(BodyMeasurement.user_id == current_user.id)
        .order_by(BodyMeasurement.logged_at.desc())
        .first()
    )
    if not entry:
        raise HTTPException(status_code=404, detail="No measurements logged yet")
    return entry


@router.get(
    "/stats",
    summary="Body measurement stats",
    response_description="First, latest, and change for each metric",
)
def measurement_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns a summary comparing your first ever logged measurement
    against your most recent one, showing the change for each metric.

    Great for a progress summary card on the profile screen.
    """
    entries = (
        db.query(BodyMeasurement)
        .filter(BodyMeasurement.user_id == current_user.id)
        .order_by(BodyMeasurement.logged_at)
        .all()
    )
    if not entries:
        return {"message": "No measurements logged yet", "stats": {}}

    first  = entries[0]
    latest = entries[-1]

    fields = ["weight_kg", "body_fat_pct", "chest_cm", "waist_cm",
              "hips_cm", "arms_cm", "legs_cm"]

    stats = {}
    for field in fields:
        first_val  = getattr(first, field)
        latest_val = getattr(latest, field)
        if first_val is not None and latest_val is not None:
            stats[field] = {
                "first":   round(first_val, 2),
                "latest":  round(latest_val, 2),
                "change":  round(latest_val - first_val, 2),
            }

    return {
        "first_logged":  first.logged_at,
        "latest_logged": latest.logged_at,
        "total_entries": len(entries),
        "stats": stats,
    }


@router.get(
    "/{entry_id}",
    response_model=BodyMeasurementOut,
    summary="Get a single measurement entry",
    responses={404: {"description": "Entry not found"}},
)
def get_measurement(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    entry = db.query(BodyMeasurement).filter(
        BodyMeasurement.id == entry_id,
        BodyMeasurement.user_id == current_user.id,
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


@router.patch(
    "/{entry_id}",
    response_model=BodyMeasurementOut,
    summary="Update a measurement entry",
    responses={404: {"description": "Entry not found"}},
)
def update_measurement(
    entry_id: int,
    payload: BodyMeasurementUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update any fields on an existing measurement entry."""
    entry = db.query(BodyMeasurement).filter(
        BodyMeasurement.id == entry_id,
        BodyMeasurement.user_id == current_user.id,
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(entry, field, value)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete(
    "/{entry_id}",
    status_code=204,
    summary="Delete a measurement entry",
    responses={404: {"description": "Entry not found"}},
)
def delete_measurement(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a single measurement entry."""
    entry = db.query(BodyMeasurement).filter(
        BodyMeasurement.id == entry_id,
        BodyMeasurement.user_id == current_user.id,
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(entry)
    db.commit()