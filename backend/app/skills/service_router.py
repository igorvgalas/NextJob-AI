"""Service-only skill endpoints protected by service token."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app import models
from app.database import get_db
from app.helpers.service_token_verifire import verify_service_token
from app.schemas import schemas

router = APIRouter(
    prefix="/service/user_skills",
    tags=["service:user-skills"],
    dependencies=[Depends(verify_service_token)],
)


@router.get("/user/{user_id}", response_model=schemas.UserSkill)
async def get_user_skills_by_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
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
