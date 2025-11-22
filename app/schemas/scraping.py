"""
Schemas para Scraping
"""
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema, ResponseBase


class ScrapingRequest(BaseSchema):
    """Request para iniciar scraping"""
    hotel_id: UUID
    plataforma_codigo: str = Field(..., pattern="^(GOOGLE|BOOKING|AIRBNB|TRIPADVISOR)$")
    url: str
    max_resenas: Optional[int] = Field(100, ge=1, le=1000)


class ScrapingStatus(BaseSchema):
    """Estado de un scraping"""
    job_id: str
    status: str  # PENDING, STARTED, SUCCESS, FAILURE
    total_extraidas: int = 0
    total_procesadas: int = 0
    errores: List[str] = []
    inicio: Optional[datetime] = None
    fin: Optional[datetime] = None


class ScrapingResponse(ResponseBase):
    """Response de inicio de scraping"""
    job_id: str
    message: str = "Scraping iniciado correctamente"


class ScrapingResult(BaseSchema):
    """Resultado de un scraping"""
    total_extraidas: int
    total_nuevas: int
    total_duplicadas: int
    total_procesadas: int
    errores: List[str] = []
    tiempo_ejecucion: float
