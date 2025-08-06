import os
import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from fastapi_users.exceptions import UserNotExists
from app.schemas.schemas import UserCreate
from app.database import get_db
from fastapi_users.password import PasswordHelper
from app.auth.auth import auth_backend
from app.auth.auth import get_user_manager
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.authentication.strategy.jwt import JWTStrategy

from app.helpers.create_refresh_token import create_refresh_token

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

    # Save Gmail access credentials
    if email:
        try:
            with open(CREDENTIALS_PATH, "r", encoding="utf-8") as f:
                all_credentials = json.load(f)
        except Exception:
            all_credentials = {}

        all_credentials[email] = {
            "access_token": data.accessToken,
            "refresh_token": data.refreshToken,
        }

        with open(CREDENTIALS_PATH, "w", encoding="utf-8") as f:
            json.dump(all_credentials, f, indent=2)

    # Check if user exists
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
