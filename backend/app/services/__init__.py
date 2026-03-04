"""
Servicios de negocio
"""
from app.services.nlp_service import nlp_service
from app.services.scraping_service import scraping_service
from app.services.indicadores_service import indicadores_service
from app.services.export_service import export_service

__all__ = [
    "nlp_service",
    "scraping_service",
    "indicadores_service",
    "export_service",
]
