from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..db import get_db

router = APIRouter()

@router.post("/study_sessions", response_model=schemas.StudySessionOut)
def log_study_session(
    session: schemas.StudySessionCreate,
    db: Session = Depends(get_db)
):
    user_id = 1 # Hardcoded for now

    # --- START VALIDATION BLOCK ---
    if session.task_id is not None:
        task = crud.get_task(db=db, task_id=session.task_id)
        if not task:
            # If task does not exist, raise a 404 Not Found error
            raise HTTPException(status_code=404, detail=f"Task with id {session.task_id} not found")
        
        # Optional: Check if the task belongs to the user
        # if task.user_id != user_id:
        #     raise HTTPException(status_code=403, detail="Not authorized to log session for this task")
    # --- END VALIDATION BLOCK ---
        
    return crud.create_study_session(db=db, session=session, user_id=user_id)