from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..db import get_db

router = APIRouter()

@router.post("/tasks", response_model=schemas.TaskOut)
def create_new_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    user_id = 1 # Hardcode for now
    return crud.create_task(db=db, task=task, user_id=user_id)