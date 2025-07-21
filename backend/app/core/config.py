"""
Core configuration for Harv v2.0
Clean, production-ready settings management
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import secrets

class Settings(BaseSettings):
    # App Info
    app_name: str = "Harv v2.0 - Intelligent Tutoring System"
    version: str = "2.0.0"
    debug: bool = False

    # Database
    database_url: str = "sqlite:///./harv_v2.db"

    # Security
    secret_key: str = secrets.token_urlsafe(32)  # Auto-generate if not provided
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    
    # CORS - Allow frontend access
    cors_origins: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]
    
    # API Settings
    api_prefix: str = "/api/v1"
    
    # Memory System Settings
    memory_max_context_length: int = 4000
    memory_fallback_enabled: bool = True
    
    # Socratic Teaching Settings
    socratic_mode_enabled: bool = True
    prevent_direct_answers: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
