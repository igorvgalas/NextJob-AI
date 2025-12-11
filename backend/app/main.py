"""
FastAPI main application module.

This module contains the main FastAPI application instance and configuration.
"""

# Load environment variables BEFORE importing modules that read env at import-time
import os
import logging
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.routes import router
from app.auth.router import router as auth_router
from app.rag.router import router as rag_router
from app.users.router import router as users_router


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',') if os.getenv('ALLOWED_HOSTS') else []

app = FastAPI(debug=True, title="NextJob AI API", version="1.0.0")


@app.middleware("http")
async def log_requests(request, call_next):
    logger.info("Request: %s %s", request.method, request.url)
    response = await call_next(request)
    logger.info("Response: %s", response.status_code)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router)
app.include_router(rag_router)
