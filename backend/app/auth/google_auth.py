from httpx import AsyncClient
from pydantic import BaseModel

from app.config import settings

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


class GoogleTokenResponse(BaseModel):
    access_token: str
    expires_in: int
    refresh_token: str | None = None
    scope: str
    token_type: str
    id_token: str | None = None


async def exchange_code_for_tokens(code: str, code_verifier: str | None = None) -> GoogleTokenResponse:
    data: dict[str, str] = {
        "client_id": settings.google_client_id or "",
        "client_secret": settings.google_client_secret or "",
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": settings.google_redirect_uri or "",
    }

    if code_verifier:
        data["code_verifier"] = code_verifier

    async with AsyncClient() as client:
        resp = await client.post(GOOGLE_TOKEN_URL, data=data)
        resp.raise_for_status()
        return GoogleTokenResponse(**resp.json())


async def get_google_userinfo(access_token: str) -> dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    async with AsyncClient() as client:
        resp = await client.get(GOOGLE_USERINFO_URL, headers=headers)
        resp.raise_for_status()
        return resp.json()
