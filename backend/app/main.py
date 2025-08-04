import os
from fastapi import FastAPI, Request
from app.routes.routes import router  # Import the router
from app.auth.auth import fastapi_users, auth_backend
# Import your Pydantic models
from app.schemas.schemas import UserRead, UserCreate, UserUpdate
from app.routes import google_auth 
from app.routes import auth_refresh
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',') if os.getenv('ALLOWED_HOSTS') else []

class AllowedHostsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        host = request.headers.get("host", "").split(":")[0]
        if host not in ALLOWED_HOSTS:
            return JSONResponse(status_code=403, content={"detail": "Host not allowed"})
        return await call_next(request)

app = FastAPI()
app.add_middleware(AllowedHostsMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

app.include_router(google_auth.router, prefix="/auth", tags=["auth"])

app.include_router(auth_refresh.router, prefix="/auth", tags=["auth"])

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}
