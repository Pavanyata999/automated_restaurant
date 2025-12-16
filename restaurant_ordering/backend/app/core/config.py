from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Restaurant Ordering System"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    SQLITE_DB: str = "sqlite:///./sql_app.db"
    DATABASE_URI: str = SQLITE_DB
    
    # First superuser
    FIRST_SUPERUSER: str = "admin@restaurant.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin123"
    
    class Config:
        case_sensitive = True

settings = Settings()
