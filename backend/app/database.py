"""
Database configuration and session management for the FastAPI application.

This module contains database connection setup and session management utilities.
"""
import os
from typing import AsyncGenerator
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# Load environment variables
load_dotenv()

DB_ENGINE = os.getenv("DB_ENGINE", "postgresql")
DB_NAME = os.getenv("DB_NAME", "dbname")
DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD", "password"))
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

DATABASE_URL = f"{DB_ENGINE}+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Base(DeclarativeBase):
    """Base class for all database models."""


# Async engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Async sessionmaker
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)


# Dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Database session dependency for FastAPI."""
    async with AsyncSessionLocal() as session:
        yield session
