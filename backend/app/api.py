from fastapi import APIRouter
from .routes import health, users

# This is the main router that will aggregate all other routers.
router = APIRouter()

# Include specific routers here. Tags are used to group endpoints in the docs.
router.include_router(health.router, tags=["Health"])
router.include_router(users.router, tags=["Users"]) # <-- Include the users router