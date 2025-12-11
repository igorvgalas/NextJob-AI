"""Aggregates service-scoped API routes protected by service token middleware."""
from fastapi import APIRouter

from app.integrations.router import router as integrations_router
from app.jobs.router import service_router as job_service_router
from app.skills.service_router import router as skill_service_router

router = APIRouter()
router.include_router(integrations_router)
router.include_router(job_service_router)
router.include_router(skill_service_router)
