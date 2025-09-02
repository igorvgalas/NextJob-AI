from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from fastapi import Request
from jose import jwt, JWTError
from services.service_auth.config import JWT_SECRET, JWT_ALGORITHM


class ServiceAuthMiddleware(BaseHTTPMiddleware):
    """Middleware to protect only /service routes with a service token.

    - Checks Authorization: Bearer <token>
    - Verifies JWT and requires payload.scope == "service"
    - Skips non-/service paths
    """

    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if path.startswith("/service"):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JSONResponse(status_code=401, content={"detail": "Missing or invalid token"})

            token = auth_header.split(" ", 1)[1]
            try:
                payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
                if payload.get("scope") != "service":
                    return JSONResponse(status_code=403, content={"detail": "Invalid token scope"})
                # Optionally expose payload to downstream handlers
                request.state.service_token_payload = payload
            except JWTError:
                return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        return await call_next(request)
