"""Integration-facing endpoints (service scope)."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app import models
from app.database import get_db
from app.helpers.service_token_verifire import verify_service_token

router = APIRouter(
    prefix="/service", tags=["service:integrations"], dependencies=[Depends(verify_service_token)]
)


@router.get("/google-creds/all", response_model=dict)
async def get_all_google_credentials(
    db: AsyncSession = Depends(get_db),
):
    stmt = select(models.GoogleCredentials).options(selectinload(models.GoogleCredentials.user))
    result = await db.execute(stmt)

    creds_dict = {}
    for creds in result.scalars().all():
        creds_dict[creds.user.email] = {
            "access_token": creds.access_token,
            "refresh_token": creds.refresh_token,
            "user_id": creds.user_id,
        }

    return creds_dict
