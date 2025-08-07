# Pydantic schemas for service auth
from pydantic import BaseModel

class TokenRequest(BaseModel):
    service_name: str
    service_secret: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
