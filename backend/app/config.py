"""
Application Configuration
"""

from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
    # Database
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://hugo:hugo_secure_password@localhost:5432/hugo_db"
    )
    
    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # ChromaDB
    chroma_url: str = os.getenv("CHROMA_URL", "http://localhost:8000")
    
    # Model servers
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    lm_studio_base_url: str = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234")
    
    # API
    api_title: str = "HUGO AI Operating System"
    api_version: str = "1.0.0"
    api_port: int = int(os.getenv("API_PORT", 8001))
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    
    # Security
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "change-this-in-production")
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8001"]
    
    # Voice
    voice_enabled: bool = os.getenv("VOICE_ENABLED", "true").lower() == "true"
    wake_word: str = os.getenv("WAKE_WORD", "hugo")
    speech_recognition_model: str = os.getenv("SPEECH_RECOGNITION_MODEL", "base")
    text_to_speech_model: str = os.getenv("TEXT_TO_SPEECH_MODEL", "tts-1")
    
    # Models
    default_model: str = os.getenv("DEFAULT_MODEL", "mistral")
    max_tokens: int = 2048
    temperature: float = 0.7
    
    # Features
    enable_auto_learning: bool = os.getenv("ENABLE_AUTO_LEARNING", "true").lower() == "true"
    enable_memory_persistence: bool = os.getenv("ENABLE_MEMORY_PERSISTENCE", "true").lower() == "true"
    enable_browser_automation: bool = os.getenv("ENABLE_BROWSER_AUTOMATION", "true").lower() == "true"
    enable_code_execution: bool = os.getenv("ENABLE_CODE_EXECUTION", "true").lower() == "true"
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    # File paths
    data_dir: str = os.getenv("DATA_DIR", "./data")
    models_dir: str = f"{os.getenv('DATA_DIR', './data')}/models"
    documents_dir: str = f"{os.getenv('DATA_DIR', './data')}/documents"
    logs_dir: str = f"{os.getenv('DATA_DIR', './data')}/logs"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
