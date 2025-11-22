"""
Configuración centralizada de la aplicación con Pydantic Settings
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Configuración de la aplicación ScrapingWeb"""
    
    # Información del Proyecto
    PROJECT_NAME: str = "ScrapingWeb - Pymes Hoteleras Barranquilla"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API para scraping y análisis de reseñas hoteleras"
    API_PREFIX: str = "/api/v1"
    
    # Database PostgreSQL
    POSTGRES_USER: str = "scrapingweb_user"
    POSTGRES_PASSWORD: str = "scrapingweb_pass_2025"
    POSTGRES_DB: str = "scrapingweb_db"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    DATABASE_URL: str = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    
    # Redis & Celery
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
    CELERY_BROKER_URL: str = REDIS_URL
    CELERY_RESULT_BACKEND: str = REDIS_URL
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-in-production-2025"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 horas
    
    # Scraping Configuration
    SCRAPING_TIMEOUT: int = 300  # 5 minutos
    SCRAPING_MAX_RETRIES: int = 3
    SCRAPING_RETRY_DELAY: int = 5  # segundos
    CHROMEDRIVER_PATH: str = "/usr/bin/chromedriver"
    HEADLESS_BROWSER: bool = True
    
    # NLP Configuration
    SPACY_MODEL: str = "es_core_news_sm"
    SENTIMENT_THRESHOLD_POSITIVE: float = 0.2
    SENTIMENT_THRESHOLD_NEGATIVE: float = -0.2
    
    # Export Configuration
    EXPORT_DIR: str = "exports"
    EXPORT_MAX_AGE_DAYS: int = 7  # Archivos expiran en 7 días
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5000,http://127.0.0.1:3000,http://127.0.0.1:5000"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convierte CORS_ORIGINS en lista"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Obtener instancia singleton de configuración
    """
    return Settings()


settings = get_settings()
