import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.allowed_hosts import AllowedHostsMiddleware
from .router import router as service_auth_router


ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',') if os.getenv('ALLOWED_HOSTS') else []
app = FastAPI(debug=True, title="Auth Service", version="1.0.0")

app.add_middleware(AllowedHostsMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(service_auth_router, prefix="/auth", tags=["auth"])
