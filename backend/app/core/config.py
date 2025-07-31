from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings and configuration"""
    
    # Application
    PROJECT_NAME: str = "AI-mVISE Repository Analyzer"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # API
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "ai-mvise-super-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/ai_mvise_db"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "ai_mvise_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # GitHub API
    GITHUB_TOKEN: Optional[str] = None
    GITHUB_API_URL: str = "https://api.github.com"
    
    # AI Services
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None
    USE_AI_SERVICE: str = "anthropic"  # "openai" or "anthropic"
    
    # Analysis Settings
    MAX_REPO_SIZE_MB: int = 1000  # Maximum repository size in MB
    ANALYSIS_TIMEOUT_MINUTES: int = 30
    MAX_CONCURRENT_ANALYSES: int = 5
    
    # File Storage
    UPLOAD_DIR: Path = Path("uploads")
    REPORTS_DIR: Path = Path("reports")
    TEMP_DIR: Path = Path("temp")
    
    # Security
    ALLOWED_HOSTS: list = ["localhost", "127.0.0.1", "0.0.0.0"]
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://localhost:3000",
    ]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "ai_mvise.log"
    
    # Analysis Thresholds
    QUALITY_SCORE_EXCELLENT: float = 8.0
    QUALITY_SCORE_GOOD: float = 6.0
    QUALITY_SCORE_FAIR: float = 4.0
    
    COMPLEXITY_THRESHOLD_HIGH: int = 15
    COMPLEXITY_THRESHOLD_MEDIUM: int = 10
    
    DUPLICATION_THRESHOLD_HIGH: float = 20.0
    DUPLICATION_THRESHOLD_MEDIUM: float = 10.0
    
    # Code Analysis Tools
    ENABLE_PYLINT: bool = True
    ENABLE_BANDIT: bool = True
    ENABLE_SAFETY: bool = True
    ENABLE_MYPY: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Create directories if they don't exist
        self.UPLOAD_DIR.mkdir(exist_ok=True)
        self.REPORTS_DIR.mkdir(exist_ok=True)
        self.TEMP_DIR.mkdir(exist_ok=True)

# Create global settings instance
settings = Settings()

# Environment-specific configurations
class DevelopmentSettings(Settings):
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"

class ProductionSettings(Settings):
    DEBUG: bool = False
    LOG_LEVEL: str = "WARNING"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")

class TestingSettings(Settings):
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./test.db"
    REDIS_URL: str = "redis://localhost:6379/1"

def get_settings() -> Settings:
    """Get settings based on environment"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProductionSettings()
    elif env == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings() 