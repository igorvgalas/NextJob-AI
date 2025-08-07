"""
Authentication router module.

This module contains all authentication-related routes including JWT auth,
user registration, Google OAuth, and refresh token functionality.
"""
import os
from fastapi import APIRouter
from jose import JWTError, jwt
from app.auth.auth import fastapi_users, auth_backend, get_user_manager
from fastapi import Depends, HTTPException, status
from fastapi_users.authentication.strategy.jwt import JWTStrategy
from app.helpers.create_refresh_token import create_refresh_token
from app.auth.google_auth import router as google_router
from app.schemas.schemas import UserCreate, UserRead, UserUpdate
from pydantic import BaseModel


# FastAPI Users default routes
from fastapi import Request, Form

# Custom login route to return both access and refresh tokens
from fastapi import APIRouter

router = APIRouter()

SECRET = os.getenv("SECRET_KEY", " ")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
router_jwt = APIRouter()

class LoginCredentials(BaseModel):
    username: str
    password: str

@router_jwt.post("/login")
async def custom_jwt_login(
    request: Request,
    user_manager=Depends(get_user_manager),
    username: str = Form(...),
    password: str = Form(...),
):
    """Custom JWT login endpoint that returns both access and refresh tokens."""
    credentials = LoginCredentials(username=username, password=password)
    user = await user_manager.authenticate(credentials)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    strategy: JWTStrategy = auth_backend.get_strategy()  # type: ignore
    access_token = await strategy.write_token(user)
    print(f"Access token generated for user {user.id} - {access_token}")
    refresh_token = create_refresh_token(user)
    return {
        "access": access_token,
        "refresh": refresh_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
    }

# Stateless logout endpoint
@router_jwt.post("/logout")
async def custom_logout():
    """Logout endpoint. If you store refresh tokens, invalidate them here."""
    return {"detail": "Successfully logged out"}


@router_jwt.post("/refresh")
async def refresh_access_token(request: Request, user_manager=Depends(get_user_manager)):
    """Refresh access token using a valid refresh token."""
    data = await request.json()
    refresh_token = data.get("refresh")

    try:
        payload = jwt.decode(refresh_token, SECRET, algorithms=[ALGORITHM])
        if payload.get("scope") != "refresh_token":
            raise HTTPException(status_code=401, detail="Invalid scope")
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid refresh token") from exc

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # Load user
    user = await user_manager.get(int(user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate new access token
    strategy = auth_backend.get_strategy()
    access_token = await strategy.write_token(user) # type: ignore

    return {"access": access_token}

router.include_router(router_jwt, prefix="/jwt", tags=["auth"])
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)

# Google OAuth + Refresh Token
router.include_router(google_router)
