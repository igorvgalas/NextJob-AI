"""Aggregates public API routes for the FastAPI application."""
from fastapi import APIRouter

from app.jobs.router import router as jobs_router
from app.skills.router import router as skills_router, user_skills_router

router = APIRouter()
router.include_router(jobs_router)
router.include_router(skills_router)
router.include_router(user_skills_router)
