from fastapi import Depends, HTTPException, status, Request
from jose import jwt, JWTError
from services.service_auth.config import JWT_SECRET, JWT_ALGORITHM

def verify_service_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid token")
    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if payload.get("scope") != "service":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token scope")
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")