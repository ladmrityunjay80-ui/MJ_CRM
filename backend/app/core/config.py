"""
Application Configuration
Loads settings from environment variables
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from pathlib import Path
import os
from dotenv import load_dotenv

# Get the backend directory path
BACKEND_DIR = Path(__file__).parent.parent.parent

# Load .env file explicitly
env_file = BACKEND_DIR / ".env"
load_dotenv(env_file, override=True)


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "CRM API"
    APP_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database - Override from env with fallback
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://samikshalad@localhost:5432/crm_db")
    DATABASE_TEST_URL: str = os.getenv("DATABASE_TEST_URL", "postgresql+psycopg2://samikshalad@localhost:5432/crm_test_db")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "crm-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Email
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""
    
    model_config = SettingsConfigDict(
        env_file=str(env_file),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


# Create settings instance without caching to avoid stale values
settings = Settings()
