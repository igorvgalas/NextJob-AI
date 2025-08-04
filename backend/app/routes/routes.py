from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List
from app.schemas import schemas
from sqlalchemy.orm import selectinload
from app.models import JobOffer, Skill, UserSkill
from app.database import get_db
from app.auth.auth import fastapi_users 
from app.models import User

get_current_user = fastapi_users.current_user()
router = APIRouter()

# JobOffer Routes


@router.get("/job_offers", response_model=dict)
async def get_job_offers(
    request: Request,
    db: AsyncSession = Depends(get_db),
    limit: int = Query(20, ge=1),
    offset: int = Query(0, ge=0),
):
    total_query = await db.execute(select(func.count()).select_from(JobOffer))
    total = total_query.scalar()

    offers_query = await db.execute(
        select(JobOffer)
        .order_by(JobOffer.created_at.desc())
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
async def delete_job_offer(job_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(JobOffer).where(JobOffer.id == job_id))
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
    current_user: User = Depends(get_current_user)
):
    offers = [models.JobOffer(user_id=current_user.id, **offer.dict(exclude_unset=True)) for offer in payload.job_offers]
    db.add_all(offers)
    await db.commit()

    for offer in offers:
        await db.refresh(offer)

    return offers


# Skill Routes
@router.get("/skills", response_model=List[schemas.Skill])
async def get_skills(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Skill))
    return result.scalars().all()


@router.get("/skills/{skill_id}", response_model=schemas.Skill)
async def get_skill(skill_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Skill).where(Skill.id == skill_id))
    skill = result.scalars().first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill


@router.post("/skills", response_model=schemas.Skill)
async def create_skill(skill: schemas.SkillCreate, db: AsyncSession = Depends(get_db)):
    db_skill = Skill(**skill.dict())
    db.add(db_skill)
    await db.commit()
    await db.refresh(db_skill)
    return db_skill


# UserSkill Routes
@router.get("/user_skills", response_model=List[schemas.UserSkill])
async def get_user_skills(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserSkill))
    return result.scalars().all()


@router.get("/user_skills/user/{user_id}", response_model=schemas.UserSkill)
async def get_user_skills_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(UserSkill)
        .options(selectinload(UserSkill.skills))
        .where(UserSkill.user_id == user_id)
    )
    user_skill = result.scalars().first()
    if not user_skill:
        raise HTTPException(status_code=404, detail="UserSkill not found")
    return user_skill


@router.post("/user_skills", response_model=schemas.UserSkill)
async def create_user_skill(payload: schemas.UserSkillCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(
        select(UserSkill).where(UserSkill.user_id == payload.user_id)
    )
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="UserSkill already exists")

    # створюємо UserSkill
    user_skill = UserSkill(user_id=payload.user_id)

    # отримуємо обʼєкти Skill
    skills = await db.execute(
        select(Skill).where(Skill.id.in_(payload.skill_ids))
    )
    user_skill.skills = skills.scalars().all()

    db.add(user_skill)
    await db.commit()

    result = await db.execute(
        select(UserSkill)
        .options(selectinload(UserSkill.skills))
        .where(UserSkill.id == user_skill.id)
    )
    user_skill = result.scalars().first()

    return user_skill


@router.patch("/user_skills/{user_skill_id}", response_model=schemas.UserSkill)
async def update_user_skill(user_skill_id: int, payload: schemas.UserSkillUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(UserSkill).options(selectinload(UserSkill.skills)).where(UserSkill.id == user_skill_id)
    )
    user_skill = result.scalars().first()

    if not user_skill:
        raise HTTPException(status_code=404, detail="UserSkill not found")

    # Завантажуємо нові скіли
    skills_result = await db.execute(select(Skill).where(Skill.id.in_(payload.skill_ids)))
    new_skills = skills_result.scalars().all()

    # Оновлюємо звʼязок
    user_skill.skills.clear()
    user_skill.skills.extend(new_skills)

    await db.commit()
    await db.refresh(user_skill)

    return user_skill


# UserSkillStat Route


@router.get("/user_skill_stats", response_model=List[schemas.UserSkillStat])
async def get_user_skill_stats(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserSkill))
    stats = result.scalars().all()
    return [
        schemas.UserSkillStat(
            username=f"User {stat.user_id}", num_skills=len(stat.skills)
        )
        for stat in stats
    ]
