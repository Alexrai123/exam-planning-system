import os
from pydantic_settings import BaseSettings
from typing import List, Optional, Dict, Any
from pydantic import field_validator, PostgresDsn


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Sistem informatic pentru planificarea examenelor"
    
    # CORS Settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080", "http://127.0.0.1:3000", "http://127.0.0.1:8000", "http://127.0.0.1:49960"]
    
    # JWT Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key_here")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key_here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    
    # Database Settings
    DATABASE_URL: Optional[PostgresDsn] = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/exam_planning"
    )
    
    # Email Settings
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "smtp.example.com")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME", "your_email@example.com")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD", "your_email_password")
    MAIL_FROM: str = os.getenv("MAIL_FROM", "your_email@example.com")
    MAIL_USE_TLS: bool = os.getenv("MAIL_USE_TLS", "True").lower() == "true"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
