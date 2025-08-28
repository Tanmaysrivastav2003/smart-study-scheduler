from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, scheduler
from app.db import get_db

# For now, we'll use dummy data. Later, this will come from the DB.
from .dummy_data import get_dummy_tasks, get_dummy_timetable

router = APIRouter()

@router.get("/schedule/generate", response_model=schemas.ScheduleResponse)
def generate_schedule_for_user(db: Session = Depends(get_db)):
    """
    Generates a new 7-day study schedule for the user.
    """
    # In a real app, you would fetch these from the database for the logged-in user
    # user_id = 1 # Get from authentication token
    # tasks = db.query(models.Task).filter(models.Task.user_id == user_id).all()
    # timetable = db.query(models.TimetableEvent).filter(models.TimetableEvent.user_id == user_id).all()

    # For now, we use dummy data to test the scheduler logic
    tasks = get_dummy_tasks()
    timetable = get_dummy_timetable()

    schedule_response = scheduler.generate_greedy_schedule(tasks=tasks, timetable=timetable)
    return schedule_response