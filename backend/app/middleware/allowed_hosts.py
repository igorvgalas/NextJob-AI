from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request
import os


ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',') if os.getenv('ALLOWED_HOSTS') else []

class AllowedHostsMiddleware(BaseHTTPMiddleware):
    """Middleware to restrict access to allowed hosts only."""

    async def dispatch(self, request: Request, call_next):
        """Check if the request host is in the allowed hosts list."""
        host = request.headers.get("host", "").split(":")[0]
        print(f"Request host: {host}")
        print(f"Allowed hosts: {ALLOWED_HOSTS}")
        if host not in ALLOWED_HOSTS:
            return JSONResponse(status_code=403, content={"detail": "Host not allowed"})
        return await call_next(request)
