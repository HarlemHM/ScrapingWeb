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
    logger.info(f"­ƒÜÇ Iniciando {settings.PROJECT_NAME}")
    logger.info(f"­ƒôî Versión: {settings.VERSION}")
    logger.info(f"­ƒîì Ambiente: {settings.ENVIRONMENT}")
    logger.info(f"­ƒÉÿ PostgreSQL: {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")
    logger.info(f"­ƒô« Redis: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
    logger.info("=" * 50)
    
    try:
        # Ejecutar seeds
        logger.info("­ƒî▒ Ejecutando seeds de datos iniciales...")
        db = SessionLocal()
        try:
            init_db(db)
        finally:
            db.close()
        logger.info("Ô£à Seeds ejecutados exitosamente")
        
        logger.info("Ô£à Aplicación iniciada correctamente")
        
    except Exception as e:
        logger.error(f"ÔØî Error durante startup: {str(e)}")
        # No elevamos el error para que la app pueda iniciar
    
    yield
    
    # Shutdown
    logger.info("=" * 50)
    logger.info("­ƒøæ Cerrando aplicación...")
    logger.info("Ô£à Aplicación cerrada correctamente")
    logger.info("=" * 50)
