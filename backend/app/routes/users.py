from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session



from .. import crud, schemas  # <-- TWO dots mean "go up one directory"
from ..db import get_db

router = APIRouter()

@router.post("/users", response_model=schemas.UserOut)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    # First, check if a user with this email already exists
    # (We will implement get_user_by_email in the crud file later, for now we skip)
    
    # Create the user
    db_user = crud.create_user(db=db, user=user)
    return db_user