from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime, date
from typing import Optional, List



# Shared properties for a User
class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None

# Properties to receive via API on user creation
class UserCreate(UserBase):
    pass

# Properties to return to the client (e.g., in an API response)
class UserOut(UserBase):
    id: int
    created_at: datetime

    # This config allows Pydantic to create this schema from a SQLAlchemy model
    model_config = ConfigDict(from_attributes=True)




# Shared properties for a Task
class TaskBase(BaseModel):
    title: str
    estimated_hours: float
    due_date: datetime
    priority: int = 2

# Properties to receive via API on task creation
class TaskCreate(TaskBase):
    pass

# Properties to return to the client for a Task
class TaskOut(TaskBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)




# Represents a single event in a day's schedule (e.g., a class or study block)
class ScheduleEvent(BaseModel):
    event_type: str  # e.g., "class" or "study"
    title: str
    start_time: datetime
    end_time: datetime
    task_id: Optional[int] = None  # Link to a task if it's a study session

# Represents the schedule for a single day
class DailySchedule(BaseModel):
    date: date
    events: List[ScheduleEvent]

# The top-level response model for the entire generated schedule
class ScheduleResponse(BaseModel):
    schedule: List[DailySchedule]


class StudySessionBase(BaseModel):
    start_time: datetime
    end_time: datetime
    focus_score: Optional[int] = None

class StudySessionCreate(StudySessionBase):
    task_id: Optional[int] = None

class StudySessionOut(StudySessionBase):
    id: int
    duration_minutes: int
    user_id: int
    task_id: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

class DashboardStats(BaseModel):
    total_study_hours_weekly: float
    daily_study_heatmap: dict[str, float]