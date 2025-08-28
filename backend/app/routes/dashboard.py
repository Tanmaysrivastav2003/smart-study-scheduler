from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import get_db

router = APIRouter()

@router.get("/dashboard", response_model=schemas.DashboardStats)
def get_dashboard_data(db: Session = Depends(get_db)):
    """
    Get aggregated statistics for the user's dashboard.
    """
    # Hardcode user_id for now
    user_id = 1
    return crud.get_dashboard_stats(db=db, user_id=user_id)