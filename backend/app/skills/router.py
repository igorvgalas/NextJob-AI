"""Routers for skills and user skill relationships."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app import models
from app.auth.auth import fastapi_users
from app.database import get_db
from app.schemas import schemas

get_current_user = fastapi_users.current_user()

router = APIRouter(prefix="/skills", tags=["skills"])
user_skills_router = APIRouter(prefix="/user_skills", tags=["user-skills"])


@router.get("", response_model=List[schemas.Skill])
async def get_skills(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    result = await db.execute(select(models.Skill))
    return result.scalars().all()


@router.get("/{skill_id}", response_model=schemas.Skill)
async def get_skill(
    skill_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    result = await db.execute(select(models.Skill).where(models.Skill.id == skill_id))
    skill = result.scalars().first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


@user_skills_router.get("", response_model=List[schemas.UserSkill])
async def get_user_skills(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    result = await db.execute(select(models.UserSkill))
    return result.scalars().all()


@user_skills_router.get("/user/{user_id}", response_model=schemas.UserSkill)
async def get_user_skills_by_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
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


@user_skills_router.post("", response_model=schemas.UserSkill)
async def create_user_skill(
    payload: schemas.UserSkillCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    existing = await db.execute(
        select(models.UserSkill).where(models.UserSkill.user_id == payload.user_id)
    )
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="UserSkill already exists")

    user_skill = models.UserSkill(user_id=payload.user_id)

    skills = await db.execute(
        select(models.Skill).where(models.Skill.id.in_(payload.skill_ids))
    )
    user_skill.skills = skills.scalars().all()

    db.add(user_skill)
    await db.commit()

    result = await db.execute(
        select(models.UserSkill)
        .options(selectinload(models.UserSkill.skills))
        .where(models.UserSkill.id == user_skill.id)
    )
    return result.scalars().first()


@user_skills_router.patch("/{user_skill_id}", response_model=schemas.UserSkill)
async def update_user_skill(
    user_skill_id: int,
    payload: schemas.UserSkillUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    result = await db.execute(
        select(models.UserSkill)
        .options(selectinload(models.UserSkill.skills))
        .where(models.UserSkill.id == user_skill_id)
    )
    user_skill = result.scalars().first()

    if not user_skill:
        raise HTTPException(status_code=404, detail="UserSkill not found")

    skills_result = await db.execute(
        select(models.Skill).where(models.Skill.id.in_(payload.skill_ids))
    )
    new_skills = skills_result.scalars().all()

    user_skill.skills.clear()
    user_skill.skills.extend(new_skills)

    await db.commit()
    await db.refresh(user_skill)

    return user_skill


@user_skills_router.get("/stats", response_model=List[schemas.UserSkillStat])
async def get_user_skill_stats(
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    result = await db.execute(select(models.UserSkill))
    stats = result.scalars().all()
    return [
        schemas.UserSkillStat(
            username=f"User {stat.user_id}", num_skills=len(stat.skills)
        )
        for stat in stats
    ]
