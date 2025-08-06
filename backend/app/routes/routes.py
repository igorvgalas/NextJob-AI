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

get_current_user = fastapi_users.current_user()
router = APIRouter()

# JobOffer Routes


@router.get("/job_offers", response_model=dict)
async def get_job_offers(
    request: Request,
    db: AsyncSession = Depends(get_db),
    limit: int = Query(20, ge=1),
    offset: int = Query(0, ge=0),
    current_user: models.User = Depends(get_current_user)
):
    total_query = await db.execute(select(func.count()).select_from(models.JobOffer))
    total = total_query.scalar()

    offers_query = await db.execute(
        select(models.JobOffer)
        .order_by(models.JobOffer.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    offers = offers_query.scalars().all()

    base_url = str(request.base_url).rstrip("/")
    next_url = (
        f"{base_url}/job_offers?limit={limit}&offset={offset + limit}"
        if total is not None and offset + limit < total else None
    )
    prev_url = (
        f"{base_url}/job_offers?limit={limit}&offset={max(offset - limit, 0)}"
        if offset > 0 else None
    )

    return {
        "count": total,
        "next": next_url,
        "previous": prev_url,
        "results": offers,
    }


@router.delete("/job_offers/{job_id}", response_model=schemas.JobOfferRead)
async def delete_job_offer(job_id: int, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.JobOffer).where(models.JobOffer.id == job_id))
    job_offer = result.scalars().first()
    if not job_offer:
        raise HTTPException(status_code=404, detail="Job offer not found")

    await db.delete(job_offer)
    await db.commit()
    return job_offer


@router.post("/job_offers/bulk_create", response_model=List[schemas.JobOfferRead])
async def create_job_offers_bulk(
    payload: schemas.JobOfferBulkCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    offers = [models.JobOffer(user_id=current_user.id, **offer.dict(exclude_unset=True)) for offer in payload.job_offers]
    db.add_all(offers)
    await db.commit()

    for offer in offers:
        await db.refresh(offer)

    return offers


# Skill Routes
@router.get("/skills", response_model=List[schemas.Skill])
async def get_skills(db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.Skill))
    return result.scalars().all()


@router.get("/skills/{skill_id}", response_model=schemas.Skill)
async def get_skill(skill_id: int, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.Skill).where(models.Skill.id == skill_id))
    skill = result.scalars().first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


@router.post("/skills", response_model=schemas.Skill)
async def create_skill(skill: schemas.SkillCreate, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_skill = models.Skill(**skill.dict())
    db.add(db_skill)
    await db.commit()
    await db.refresh(db_skill)
    return db_skill


# UserSkill Routes
@router.get("/user_skills", response_model=List[schemas.UserSkill])
async def get_user_skills(db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.UserSkill))
    return result.scalars().all()


@router.get("/user_skills/user/{user_id}", response_model=schemas.UserSkill)
async def get_user_skills_by_user(user_id: int, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = await db.execute(
        select(models.UserSkill)
        .options(selectinload(models.UserSkill.skills))
        .where(models.UserSkill.user_id == user_id)
    )
    user_skill = result.scalars().first()
    if not user_skill:
        raise HTTPException(status_code=404, detail="UserSkill not found")
    return user_skill


@router.post("/user_skills", response_model=schemas.UserSkill)
async def create_user_skill(payload: schemas.UserSkillCreate, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    existing = await db.execute(
        select(models.UserSkill).where(models.UserSkill.user_id == payload.user_id)
    )
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="UserSkill already exists")

    # створюємо UserSkill
    user_skill = models.UserSkill(user_id=payload.user_id)

    # отримуємо обʼєкти Skill
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
    user_skill = result.scalars().first()

    return user_skill


@router.patch("/user_skills/{user_skill_id}", response_model=schemas.UserSkill)
async def update_user_skill(user_skill_id: int, payload: schemas.UserSkillUpdate, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = await db.execute(
        select(models.UserSkill).options(selectinload(models.UserSkill.skills)).where(models.UserSkill.id == user_skill_id)
    )
    user_skill = result.scalars().first()

    if not user_skill:
        raise HTTPException(status_code=404, detail="UserSkill not found")

    # Завантажуємо нові скіли
    skills_result = await db.execute(select(models.Skill).where(models.Skill.id.in_(payload.skill_ids)))
    new_skills = skills_result.scalars().all()

    # Оновлюємо звʼязок
    user_skill.skills.clear()
    user_skill.skills.extend(new_skills)

    await db.commit()
    await db.refresh(user_skill)

    return user_skill


# UserSkillStat Route


@router.get("/user_skill_stats", response_model=List[schemas.UserSkillStat])
async def get_user_skill_stats(db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    result = await db.execute(select(models.UserSkill))
    stats = result.scalars().all()
    return [
        schemas.UserSkillStat(
            username=f"User {stat.user_id}", num_skills=len(stat.skills)
        )
        for stat in stats
    ]
