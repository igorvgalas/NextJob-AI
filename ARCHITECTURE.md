# NextJob AI — Architecture v2

This document captures the current v2 architecture after consolidating the platform into a single FastAPI backend with service-scoped routes and worker-style integrations.

## Core pieces

- **Mobile app (React Native/Expo):** The only client; communicates with the backend over HTTPS.
- **Backend API (FastAPI):** Monolith with feature modules:
  - `auth/` and `users/` for identity (FastAPI Users, JWT access/refresh).
  - `skills/` for user skills (public + service routes).
  - `jobs/` for user-facing job offers and service bulk ingestion.
  - `integrations/` for service-only helpers (e.g., Google credentials export).
  - `rag/` for Retrieval-Augmented Generation endpoints.
- **Background work:** Gmail/LinkedIn ingestion and LLM-based digest generation run as worker-style scripts but reuse the backend’s models and service endpoints.
- **Data + infra:** PostgreSQL (+ `pgvector`), Redis for ingestion/analysis messaging, environment-driven configuration.

## Security and configuration

- **User auth:** FastAPI Users issues JWT access/refresh tokens; cookies or Authorization headers are accepted by the API routes under `/auth/*` and `/users/*`.
- **Service auth:** Service-only routes (`/service/**`) depend on a signed JWT with `scope="service"`. Secrets and algorithms are read from environment variables (`SERVICE_JWT_SECRET`, `SERVICE_JWT_ALGORITHM`) and verified in `app/helpers/service_token_verifire.py`.
- **CORS:** Configured in `app/main.py` using the `ALLOWED_HOSTS` environment variable.

## Data flows

1. **User login** (mobile → backend)
   - `POST /auth/jwt/login` returns `{access, refresh}`.
   - `GET /users/me` keeps session state.

2. **Google OAuth link** (mobile → backend)
   - Mobile sends Google tokens to `POST /auth/google-login`.
   - Backend verifies, upserts the user, and stores credentials in `google_credentials`.

3. **Ingestion** (Gmail reader → backend → Gmail)
   - Worker obtains a service JWT (shared secret).
   - Calls `GET /service/google-creds/all` to fetch `{ email → {access_token, refresh_token, user_id} }`.
   - Polls Gmail, emits canonical `RawJobEmail` events to Redis `jobs` channel (optionally writes an idempotency log in DB).

4. **Analysis** (digest generator → LLM → backend)
   - Subscribes to Redis `jobs`, batches messages.
   - Looks up user skills via `GET /service/user_skills/user/{user_id}`.
   - Calls an LLM, maps results to job offers, and posts to `POST /service/job_offers/bulk_create` with `{ "job_offers": [...] }`.

5. **Serving** (mobile → backend)
   - `GET /job-offers?limit=&offset=` returns only the caller’s offers (filters by `current_user`).
   - Users can delete their own offers via `DELETE /job-offers/{job_id}`.

## Implementation map

- **Entry point:** `backend/app/main.py` wires routers, CORS, and request logging.
- **Routing:**
  - Public/user routes: `app/routes/routes.py`, `app/auth/router.py`, `app/users/router.py`, `app/skills/router.py`, `app/jobs/router.py`, `app/rag/router.py`.
  - Service routes (JWT `scope=service`): `app/routes/service_routes.py` aggregates `app/integrations/router.py`, `app/skills/service_router.py`, and `app/jobs/router.py` (bulk ingestion).
- **DB models:** `app/models.py`; database session in `app/database.py`; settings in `app/config.py`.

## Roadmap highlights

- Harden service-token issuance (rotate secrets, short-lived tokens).
- Move Gmail idempotency tracking into the database or Redis Streams consumer groups.
- Swap the LLM client to first-party SDKs with schema validation.
- Add observability (structured logs/metrics) and containerized deployment (Docker Compose).
