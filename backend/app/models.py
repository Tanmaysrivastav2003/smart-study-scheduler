# Add ForeignKey to your imports
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey ,Text
from sqlalchemy.orm import relationship # Add relationship import
from sqlalchemy.sql import func
from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Add relationships to tasks and timetable events
    tasks = relationship("Task", back_populates="owner")
    timetable_events = relationship("TimetableEvent", back_populates="owner")
    study_sessions = relationship("StudySession", back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    estimated_hours = Column(Float, nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=False)
    priority = Column(Integer, default=2)  # e.g., 1-High, 2-Medium, 3-Low
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="tasks")
    study_sessions = relationship("StudySession", back_populates="task")

class TimetableEvent(Base):
    __tablename__ = "timetable_events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    day_of_week = Column(Integer, nullable=False) # 0=Monday, 1=Tuesday, ...
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="timetable_events")
class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    focus_score = Column(Integer, nullable=True) # e.g., A score from 1-5 rated by the user
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True) # Nullable because a session might not be for a specific task

    owner = relationship("User", back_populates="study_sessions")
    task = relationship("Task", back_populates="study_sessions")