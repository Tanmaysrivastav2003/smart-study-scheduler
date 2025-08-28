from datetime import datetime, time, timedelta
from app import models

# This is a temporary way to simulate having data in our database

def get_dummy_tasks():
    """Returns a list of dummy Task objects."""
    now = datetime.now()
    return [
        models.Task(id=1, title="Maths Homework", estimated_hours=3, due_date=now + timedelta(days=2), priority=1, user_id=1),
        models.Task(id=2, title="Physics Project", estimated_hours=8, due_date=now + timedelta(days=5), priority=2, user_id=1),
        models.Task(id=3, title="History Reading", estimated_hours=2, due_date=now + timedelta(days=3), priority=3, user_id=1),
    ]

def get_dummy_timetable():
    """Returns a list of dummy TimetableEvent objects."""
    return [
        # Monday 9:00 - 10:30 AM class
        models.TimetableEvent(id=1, title="Calculus", day_of_week=0, start_time=datetime.combine(datetime.today(), time(9, 0)), end_time=datetime.combine(datetime.today(), time(10, 30)), user_id=1),
        # Wednesday 1:00 - 3:00 PM class
        models.TimetableEvent(id=2, title="Physics Lab", day_of_week=2, start_time=datetime.combine(datetime.today(), time(13, 0)), end_time=datetime.combine(datetime.today(), time(15, 0)), user_id=1),
    ]