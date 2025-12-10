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
import asyncio
import time
from fastapi.middleware.cors import CORSMiddleware
from app.auth.auth import fastapi_users
from app.middleware.allowed_hosts import AllowedHostsMiddleware
from app.middleware.service_token_middleware import ServiceAuthMiddleware
from app.schemas.schemas import UserRead, UserUpdate
from app.routes.routes import router
from app.auth.router import router as auth_router
from app.routes.service_routes import router as service_routes


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(
    ',') if os.getenv('ALLOWED_HOSTS') else []

app = FastAPI(debug=True, title="NextJob AI API", version="1.0.0")


@app.middleware("http")
async def log_requests(request, call_next):
    logger.info("Request: %s %s", request.method, request.url)
    response = await call_next(request)
    logger.info("Response: %s", response.status_code)
    return response

app.add_middleware(AllowedHostsMiddleware)
app.add_middleware(ServiceAuthMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, tags=["api"])

app.include_router(auth_router, prefix="/auth", tags=["auth"])

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"]
)

app.include_router(service_routes, prefix="/service", tags=["service"])
