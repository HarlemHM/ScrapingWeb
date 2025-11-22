"""
Eventos de ciclo de vida de la aplicación
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.logging_config import logger
from app.core.config import settings
from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.seeds.initial_data import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manejo de eventos startup y shutdown de la aplicación
    """
    # Startup
    logger.info("=" * 50)
    logger.info(f"🚀 Iniciando {settings.PROJECT_NAME}")
    logger.info(f"📌 Versión: {settings.VERSION}")
    logger.info(f"🌍 Ambiente: {settings.ENVIRONMENT}")
    logger.info(f"🐘 PostgreSQL: {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")
    logger.info(f"📮 Redis: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
    logger.info("=" * 50)
    
    try:
        # Ejecutar seeds
        logger.info("🌱 Ejecutando seeds de datos iniciales...")
        db = SessionLocal()
        try:
            init_db(db)
        finally:
            db.close()
        logger.info("✅ Seeds ejecutados exitosamente")
        
        logger.info("✅ Aplicación iniciada correctamente")
        
    except Exception as e:
        logger.error(f"❌ Error durante startup: {str(e)}")
        # No elevamos el error para que la app pueda iniciar
    
    yield
    
    # Shutdown
    logger.info("=" * 50)
    logger.info("🛑 Cerrando aplicación...")
    logger.info("✅ Aplicación cerrada correctamente")
    logger.info("=" * 50)
