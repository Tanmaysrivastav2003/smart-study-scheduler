from fastapi import APIRouter
from app.routes import health


router = APIRouter()


router.include_router(health.router, tags=["Health"])