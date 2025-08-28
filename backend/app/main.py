from fastapi import FastAPI
from .api import router

app = FastAPI(
    title="Smart Study Scheduler API",
    description="API for managing schedules, tasks, and predicting student burnout.",
    version="0.1.0"
)

# Include the main API router
app.include_router(router, prefix="/api/v1")