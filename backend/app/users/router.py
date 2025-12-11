"""User management router wrapper for FastAPI Users."""
from fastapi import APIRouter

from app.auth.auth import fastapi_users
from app.schemas.schemas import UserRead, UserUpdate

router = APIRouter()
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
