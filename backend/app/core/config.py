from pydantic import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/abide"
    REDIS_URL: str = "redis://localhost:6379"
    
    # API Keys
    YOUTUBE_API_KEY: str = ""
    OPENAI_API_KEY: Optional[str] = None
    
    # App Configuration
    BIBLE_PROVIDER: str = "public_domain"  # public_domain, esv, niv
    APP_SECRET_KEY: str = "change_this_in_production"
    ENVIRONMENT: str = "development"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Supabase
    SUPABASE_URL: Optional[str] = None
    SUPABASE_ANON_KEY: Optional[str] = None
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = None
    
    # Content Settings
    MAX_REFLECTION_LENGTH: int = 160
    MAX_DEVOTION_REFLECTION_LENGTH: int = 250
    MAX_SCRIPTURE_VERSES: int = 6
    
    # YouTube Settings
    YOUTUBE_SAFE_SEARCH: str = "strict"
    YOUTUBE_MAX_DURATION: int = 600  # 10 minutes in seconds
    YOUTUBE_MIN_DURATION: int = 180  # 3 minutes in seconds
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# Override CORS origins if environment variable is set
if os.getenv("CORS_ORIGINS"):
    settings.CORS_ORIGINS = os.getenv("CORS_ORIGINS").split(",")
