from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Workout(Base):
    __tablename__ = "workouts"

    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False)
    title        = Column(String, nullable=False)
    notes        = Column(Text)
    scheduled_at = Column(DateTime(timezone=True))
    status       = Column(String, default="pending")  # pending | completed | skipped
    created_at   = Column(DateTime(timezone=True), server_default=func.now())

    owner     = relationship("User", back_populates="workouts")
    exercises = relationship("WorkoutExercise", back_populates="workout", cascade="all, delete")

class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id            = Column(Integer, primary_key=True, index=True)
    workout_id    = Column(Integer, ForeignKey("workouts.id"), nullable=False)
    exercise_id   = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    sets          = Column(Integer)
    reps          = Column(Integer)
    weight_kg     = Column(Float)
    duration_secs = Column(Integer)
    notes         = Column(Text)

    workout  = relationship("Workout", back_populates="exercises")
    exercise = relationship("Exercise")

class PersonalRecord(Base):
    __tablename__ = "personal_records"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    record_type = Column(String, nullable=False)  # max_weight | max_reps | max_volume
    value       = Column(Float, nullable=False)
    achieved_at = Column(DateTime(timezone=True), server_default=func.now())

    user     = relationship("User")
    exercise = relationship("Exercise")

class WorkoutTemplate(Base):
    __tablename__ = "workout_templates"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    title      = Column(String, nullable=False)
    notes      = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user      = relationship("User")
    exercises = relationship("TemplateExercise", back_populates="template", cascade="all, delete")

class TemplateExercise(Base):
    __tablename__ = "template_exercises"

    id            = Column(Integer, primary_key=True, index=True)
    template_id   = Column(Integer, ForeignKey("workout_templates.id"), nullable=False)
    exercise_id   = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    sets          = Column(Integer)
    reps          = Column(Integer)
    weight_kg     = Column(Float)
    duration_secs = Column(Integer)
    notes         = Column(Text)

    template = relationship("WorkoutTemplate", back_populates="exercises")
    exercise = relationship("Exercise")

class BodyMeasurement(Base):
    __tablename__ = "body_measurements"

    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False)
    logged_at    = Column(DateTime(timezone=True), server_default=func.now())
    weight_kg    = Column(Float, nullable=True)
    body_fat_pct = Column(Float, nullable=True)
    chest_cm     = Column(Float, nullable=True)
    waist_cm     = Column(Float, nullable=True)
    hips_cm      = Column(Float, nullable=True)
    arms_cm      = Column(Float, nullable=True)
    legs_cm      = Column(Float, nullable=True)
    notes        = Column(Text, nullable=True)

    user = relationship("User")

