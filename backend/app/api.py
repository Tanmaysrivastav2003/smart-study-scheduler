from fastapi import APIRouter
# Import dashboard
from .routes import health, users, schedule, study_sessions, dashboard, tasks

router = APIRouter()

router.include_router(health.router, tags=["Health"])
router.include_router(users.router, tags=["Users"])
router.include_router(schedule.router, tags=["Schedule"])
router.include_router(study_sessions.router, tags=["Study Sessions"])
router.include_router(dashboard.router, tags=["Dashboard"]) # <-- Include router
router.include_router(tasks.router, tags=["Tasks"])