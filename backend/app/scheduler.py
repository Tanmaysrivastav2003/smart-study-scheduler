from datetime import datetime, timedelta, time
from typing import List, Dict
from . import schemas, models

# --- Constants for the scheduler ---
STUDY_CHUNK_MINUTES = 50
BREAK_MINUTES = 10
MAX_CONTINUOUS_STUDY_CHUNKS = 2

def generate_greedy_schedule(
    tasks: List[models.Task],
    timetable: List[models.TimetableEvent],
    horizon_days: int = 7,
    start_of_day: time = time(8, 0),   # 8 AM
    end_of_day: time = time(22, 0)     # 10 PM
) -> schemas.ScheduleResponse:
    """
    Generates a study schedule using a greedy algorithm.
    """
    # 1. Chunk all tasks into 50-minute study blocks
    study_chunks = []
    for task in tasks:
        num_chunks = int(task.estimated_hours * 60 / STUDY_CHUNK_MINUTES)
        for _ in range(num_chunks):
            study_chunks.append({
                "task_id": task.id,
                "title": task.title,
                "due_date": task.due_date,
                "priority": task.priority
            })

    # 2. Sort chunks by urgency (due date first, then priority)
    # This is the "greedy" part: we always schedule the most urgent chunk first.
    study_chunks.sort(key=lambda x: (x['due_date'], x['priority']))
    
    # 3. Build the schedule day by day for the next `horizon_days`
    full_schedule = []
    today = datetime.now().date()

    for i in range(horizon_days):
        current_date = today + timedelta(days=i)
        daily_events = []
        
        # Start the day at the defined start_of_day time
        current_time = datetime.combine(current_date, start_of_day)
        
        # Add existing timetable events (classes) for that day
        day_of_week = current_date.weekday() # Monday is 0
        for event in timetable:
            if event.day_of_week == day_of_week:
                daily_events.append(schemas.ScheduleEvent(
                    event_type="class",
                    title=event.title,
                    start_time=event.start_time.replace(year=current_date.year, month=current_date.month, day=current_date.day),
                    end_time=event.end_time.replace(year=current_date.year, month=current_date.month, day=current_date.day),
                ))

        # Sort all events to easily find free time slots
        daily_events.sort(key=lambda x: x.start_time)

        # 4. Fill free slots with study chunks
        continuous_chunks_done = 0
        scheduled_this_day = []

        while current_time.time() < end_of_day and study_chunks:
            slot_end_time = current_time + timedelta(minutes=STUDY_CHUNK_MINUTES)

            # Check if this slot is free
            is_slot_free = True
            for event in daily_events:
                # Simple overlap check
                if max(current_time, event.start_time) < min(slot_end_time, event.end_time):
                    is_slot_free = False
                    # Jump current_time to the end of the blocking event
                    current_time = event.end_time
                    break
            
            if is_slot_free:
                # If the slot is free, schedule the most urgent chunk
                chunk_to_schedule = study_chunks.pop(0)
                
                study_event = schemas.ScheduleEvent(
                    event_type="study",
                    title=chunk_to_schedule['title'],
                    start_time=current_time,
                    end_time=slot_end_time,
                    task_id=chunk_to_schedule['task_id']
                )
                scheduled_this_day.append(study_event)
                
                current_time = slot_end_time # Move time forward
                continuous_chunks_done += 1
                
                # Add a break if we've studied for too long continuously
                if continuous_chunks_done >= MAX_CONTINUOUS_STUDY_CHUNKS:
                    current_time += timedelta(minutes=BREAK_MINUTES)
                    continuous_chunks_done = 0

        # Add the scheduled study blocks to the daily events
        daily_events.extend(scheduled_this_day)
        daily_events.sort(key=lambda x: x.start_time)
        
        full_schedule.append(schemas.DailySchedule(date=current_date, events=daily_events))
    
    return schemas.ScheduleResponse(schedule=full_schedule)