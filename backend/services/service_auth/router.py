from fastapi import APIRouter, Depends, HTTPException
from .schemas import TokenRequest, TokenResponse
from .utils import create_jwt_token
from .config import SERVICE_CREDENTIALS

router = APIRouter()

@router.post("/token", response_model=TokenResponse)
def get_service_token(request: TokenRequest):
    creds = SERVICE_CREDENTIALS.get(request.service_name)
    if not creds or creds["secret"] != request.service_secret:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt_token(service_name=request.service_name)
    return TokenResponse(access_token=token, token_type="bearer")