from jose import jwt
from datetime import datetime, timedelta
from app.models import User  # or wherever your User model is
import os


# Should match your secret and lifetime setup
SECRET = os.getenv("SECRET_KEY", "CHANGE_THIS_SECRET")
REFRESH_TOKEN_LIFETIME_DAYS = os.getenv("REFRESH_TOKEN_LIFETIME_DAYS", 7)
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def create_refresh_token(user: User) -> str:
    expire = datetime.utcnow() + timedelta(days=float(REFRESH_TOKEN_LIFETIME_DAYS))
    to_encode = {
        "sub": str(user.id),
        "exp": expire,
        "scope": "refresh_token",
    }
    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)