from fastapi import APIRouter, HTTPException, Request
from jose import JWTError, jwt
from app.auth.auth import auth_backend, fastapi_users
import os

# Load environment variables
SECRET = os.getenv("SECRET_KEY", " ")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

router = APIRouter()

@router.post("/refresh")
async def refresh_access_token(request: Request):
    data = await request.json()
    refresh_token = data.get("refresh")

    try:
        payload = jwt.decode(refresh_token, SECRET, algorithms=[ALGORITHM])
        if payload.get("scope") != "refresh_token":
            raise HTTPException(status_code=401, detail="Invalid scope")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # Load user
    user = fastapi_users.current_user()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate new access token
    strategy = auth_backend.get_strategy()
    access_token = await strategy.write_token(user) # type: ignore

    return {"access": access_token}
