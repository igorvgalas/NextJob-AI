import os


class Settings:
    DATABASE_URL = os.getenv(
        "DATABASE_URL", "postgresql://user:password@localhost/dbname")
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM = "HS256"


settings = Settings()
