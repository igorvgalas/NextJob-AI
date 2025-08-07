import os
from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend, BearerTransport
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.manager import BaseUserManager
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.database import get_db


SECRET = os.getenv("SECRET_KEY", "")
ACCESS_TOKEN_LIFETIME_MINUTES = os.getenv("ACCESS_TOKEN_LIFETIME_MINUTES", 15)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=int(ACCESS_TOKEN_LIFETIME_MINUTES) * 60)


bearer_transport = BearerTransport(tokenUrl="/auth/jwt/login")

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(BaseUserManager[User, int]):
    user_db_model = User
    
    def parse_id(self, user_id: str) -> int:
        return int(user_id)
    
async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager=get_user_manager,
    auth_backends=[auth_backend],
)
