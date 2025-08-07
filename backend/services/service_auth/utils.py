# JWT helpers for service auth
import jwt
from datetime import datetime, timedelta
from .config import JWT_SECRET, JWT_ALGORITHM

def create_jwt_token(service_name: str) -> str:
    payload = {
        "sub": service_name,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1),
        "scope": "service"
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
