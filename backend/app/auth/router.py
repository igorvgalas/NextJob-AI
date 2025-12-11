"""
Authentication router module.

This module contains all authentication-related routes including JWT auth,
user registration, Google OAuth, and refresh token functionality.
"""
import os
from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.authentication.strategy.jwt import JWTStrategy
from fastapi_users.password import PasswordHelper
from pydantic import BaseModel

from app import models
from app.auth.auth import fastapi_users, auth_backend, get_user_manager
from app.auth.google_auth import exchange_code_for_tokens, get_google_userinfo
from app.database import get_db
from app.helpers.create_refresh_token import create_refresh_token
from app.schemas.schemas import UserCreate, UserRead, UserUpdate

router = APIRouter()

SECRET = os.getenv("SECRET_KEY", " ")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
router_jwt = APIRouter()
password_helper = PasswordHelper()


class LoginCredentials(BaseModel):
    username: str
    password: str


class GoogleCodeIn(BaseModel):
    code: str
    code_verifier: str | None = None


async def _issue_app_tokens(user, created: bool = False) -> dict:
    strategy: JWTStrategy = auth_backend.get_strategy()  # type: ignore
    access_token = await strategy.write_token(user)
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
        },
        "created": created,
    }


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

    tokens = await _issue_app_tokens(user)
    tokens.pop("created", None)
    return tokens


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

    user = await user_manager.get(int(user_id))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    strategy = auth_backend.get_strategy()
    access_token = await strategy.write_token(user)  # type: ignore

    return {"access": access_token}


@router.post("/google/exchange-code")
async def google_exchange_code(
    payload: GoogleCodeIn,
    session: AsyncSession = Depends(get_db),
    user_manager=Depends(get_user_manager),
):
    """Exchange Google OAuth code for tokens and issue app credentials."""
    tokens = await exchange_code_for_tokens(payload.code, payload.code_verifier)

    userinfo = await get_google_userinfo(tokens.access_token)
    email = userinfo.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Google did not return email")

    result = await session.execute(select(models.User).where(models.User.email == email))
    user = result.scalar_one_or_none()
    created = False

    if user is None:
        user = await user_manager.create(
            UserCreate(
                email=email,
                password=password_helper.hash("google-oauth"),
                first_name=userinfo.get("given_name") or userinfo.get("name"),
                last_name=userinfo.get("family_name"),
            ),
            safe=True,
            request=None,
        )
        created = True

    result = await session.execute(
        select(models.GoogleCredentials).where(models.GoogleCredentials.user_id == user.id)
    )
    creds = result.scalar_one_or_none()

    if creds is None:
        creds = models.GoogleCredentials(
            user_id=user.id,
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            scope=tokens.scope,
            token_type=tokens.token_type,
        )
        session.add(creds)
    else:
        creds.access_token = tokens.access_token
        if tokens.refresh_token:
            creds.refresh_token = tokens.refresh_token
        creds.scope = tokens.scope
        creds.token_type = tokens.token_type

    await session.commit()

    return await _issue_app_tokens(user, created=created)


router.include_router(router_jwt, prefix="/jwt", tags=["auth"])
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
