from fastapi import APIRouter

router = APIRouter()

@router.get("/health", response_model=dict)
def health_check():
    """
    A simple health check endpoint to confirm the API is running.
    """
    return {"status": "ok"}