from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List
from app.schemas import schemas
from sqlalchemy.orm import selectinload
from app import models
from app.database import get_db
from app.auth.auth import fastapi_users 
from app.helpers.service_token_verifire import verify_service_token

router = APIRouter()

@router.get("/google-creds/all", response_model=dict)
async def get_all_google_credentials(
    db: AsyncSession = Depends(get_db), 
    service_token=Depends(verify_service_token)
):
    stmt = (
        select(models.GoogleCredentials, models.User)
        .join(models.User, models.GoogleCredentials.user_id == models.User.id)
    )
    result = await db.execute(stmt)

    creds_dict = {}
    for creds, user in result.all():
        creds_dict[user.email] = {
            "access_token": creds.access_token,
            "refresh_token": creds.refresh_token,
            "user_id": creds.user_id,
        }

    return creds_dict

@router.get("/user_skills/user/{user_id}", response_model=schemas.UserSkill)
async def get_user_skills_by_user(
    user_id: int, 
    db: AsyncSession = Depends(get_db), 
    service_token = Depends(verify_service_token)
):
    result = await db.execute(
        select(models.UserSkill)
        .options(selectinload(models.UserSkill.skills))
        .where(models.UserSkill.user_id == user_id)
    )
    user_skill = result.scalars().first()
    if not user_skill:
        raise HTTPException(status_code=404, detail="UserSkill not found")
    return user_skill

@router.post("/job_offers/bulk_create", response_model=List[schemas.JobOfferRead])
async def create_job_offers_bulk(
    payload: schemas.JobOfferBulkCreate,
    db: AsyncSession = Depends(get_db),
    service_token = Depends(verify_service_token)
):
    offers = [models.JobOffer(**offer.dict(exclude_unset=True)) for offer in payload.job_offers]
    db.add_all(offers)
    await db.commit()

    for offer in offers:
        await db.refresh(offer)

    return offers