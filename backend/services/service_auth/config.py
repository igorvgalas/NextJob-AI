# Config for service auth
JWT_SECRET = "next_job_ai_jwt_secret_key_for_services"
JWT_ALGORITHM = "HS256"

# Example service credentials
SERVICE_CREDENTIALS = {
    "gmail_service": {"secret": "gmail_secret"},
    "digest_generator": {"secret": "digest_generator_secret"},
    "linkedin_service": {"secret": "linkedin_secret"}
}
