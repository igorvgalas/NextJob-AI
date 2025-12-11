"""Job domain routers for public and service APIs."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import models
from app.auth.auth import fastapi_users
from app.database import get_db
from app.schemas.schemas import JobOfferBase, JobOfferBulkCreate, JobOfferPage, JobOfferRead

get_current_user = fastapi_users.current_user()

router = APIRouter(prefix="/job-offers", tags=["jobs"])


@router.get("", response_model=JobOfferPage)
async def get_job_offers(
    request: Request,
    db: AsyncSession = Depends(get_db),
    limit: int = Query(20, ge=1),
    offset: int = Query(0, ge=0),
    current_user: models.User = Depends(get_current_user),
):
    query = select(models.JobOffer).where(models.JobOffer.user_id == current_user.id)

    total = (await db.execute(select(func.count()).select_from(query.subquery()))).scalar() or 0

    offers = (
        await db.execute(
            query.order_by(models.JobOffer.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
    ).scalars().all()

    base_url = str(request.base_url).rstrip("/")
    next_url = (
        f"{base_url}/job-offers?limit={limit}&offset={offset + limit}"
        if offset + limit < total
        else None
    )
    prev_url = (
        f"{base_url}/job-offers?limit={limit}&offset={max(offset - limit, 0)}"
        if offset > 0
        else None
    )

    results = [JobOfferBase.model_validate(o) for o in offers]

    return JobOfferPage(count=total, next=next_url, previous=prev_url, results=results)


@router.delete("/{job_id}", response_model=JobOfferRead)
async def delete_job_offer(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    result = await db.execute(select(models.JobOffer).where(models.JobOffer.id == job_id))
    job_offer = result.scalars().first()
    if not job_offer:
        raise HTTPException(status_code=404, detail="Job offer not found")
    if job_offer.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this offer")

    await db.delete(job_offer)
    await db.commit()
    return job_offer


service_router = APIRouter(
    prefix="/service/job_offers",
    tags=["service:jobs"],
    dependencies=[Depends(get_current_user)],
)


@service_router.post("/bulk_create", response_model=List[JobOfferRead])
async def create_job_offers_bulk(
    payload: JobOfferBulkCreate,
    db: AsyncSession = Depends(get_db),
):
    offers = [models.JobOffer(**offer.model_dump(exclude_unset=True)) for offer in payload.job_offers]
    db.add_all(offers)
    await db.commit()

    for offer in offers:
        await db.refresh(offer)

    return offers
