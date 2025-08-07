import os
import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi_users.authentication.strategy.jwt import JWTStrategy
from fastapi_users.exceptions import UserNotExists
from fastapi_users.password import PasswordHelper
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schemas import UserCreate
from app.database import get_db
from app.auth.auth import auth_backend
from app.auth.auth import get_user_manager
from app.helpers.create_refresh_token import create_refresh_token
from sqlalchemy import update, insert
from app.models import GoogleCredentials

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("IOS_GOOGLE_CLIENT_ID")
CREDENTIALS_PATH = "services/gmail_reader/credentials.json"
os.makedirs(os.path.dirname(CREDENTIALS_PATH), exist_ok=True)

password_helper = PasswordHelper()


class GoogleAuthRequest(BaseModel):
    id_token: str
    accessToken: str
    refreshToken: str | None = None


@router.post("/google-login")
async def google_login(
    data: GoogleAuthRequest,
    session: AsyncSession = Depends(get_db),
    user_manager=Depends(get_user_manager),
):
    try:
        idinfo = google_id_token.verify_oauth2_token(
            data.id_token, google_requests.Request(), GOOGLE_CLIENT_ID
        )
        email = idinfo.get("email")
        if not email:
            raise HTTPException(
                status_code=400, detail="Email not found in token")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid token: {e}")

    try:
        user = await user_manager.get_by_email(email)
        created = False
    except UserNotExists:
        user = await user_manager.create(
            UserCreate(
                email=email,
                password=password_helper.hash("google-oauth"),
                first_name=idinfo.get("given_name", ""),
                last_name=idinfo.get("family_name", "")
            ),
            safe=True,
            request=None,
        )
        created = True

    if email:
        stmt = (
            update(GoogleCredentials)
            .where(GoogleCredentials.user_id == user.id)
            .values(
            access_token=data.accessToken,
            refresh_token=data.refreshToken,
            updated_at=datetime.utcnow()
            )
        )
        result = await session.execute(stmt)
        if result.rowcount == 0:
            stmt = (
                insert(GoogleCredentials)
                .values(
                user_id=user.id,
                access_token=data.accessToken,
                refresh_token=data.refreshToken,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
                )
            )
            await session.execute(stmt)
        await session.commit()

    # Generate access token
    strategy: JWTStrategy = auth_backend.get_strategy()  # type: ignore
    access_token = await strategy.write_token(user)

    # Generate refresh token manually
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
