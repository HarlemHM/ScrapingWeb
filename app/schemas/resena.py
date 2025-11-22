"""
Schemas para Reseña
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class ResenaBase(BaseSchema):
    """Schema base de Reseña"""
    hotel_plataforma_id: UUID
    nombre_autor: Optional[str] = Field(None, max_length=255)
    ubicacion_autor: Optional[str] = Field(None, max_length=255)
    texto_positivo: Optional[str] = None
    texto_negativo: Optional[str] = None
    texto_completo: Optional[str] = None
    puntuacion: Optional[float] = Field(None, ge=1, le=5)
    fecha_publicacion: Optional[datetime] = None
    tipo_estadia: Optional[str] = Field(None, max_length=100)
    titulo: Optional[str] = Field(None, max_length=500)


class ResenaCreate(ResenaBase):
    """Schema para crear Reseña"""
    pass


class ResenaRead(ResenaBase):
    """Schema para leer Reseña"""
    id: UUID
    procesada: bool = False
    fecha_procesamiento: Optional[datetime] = None
    hash_contenido: Optional[str] = None
    creado_en: datetime


class SentimientoBase(BaseSchema):
    """Schema base de Sentimiento"""
    tipo_sentimiento: str = Field(..., pattern="^(POSITIVO|NEGATIVO|NEUTRO)$")
    score_positivo: float = Field(0.0, ge=0, le=1)
    score_negativo: float = Field(0.0, ge=0, le=1)
    score_neutro: float = Field(0.0, ge=0, le=1)
    score_compuesto: float = Field(0.0, ge=-1, le=1)
    confianza: float = Field(0.0, ge=0, le=1)


class SentimientoRead(SentimientoBase):
    """Schema para leer Sentimiento"""
    id: UUID
    resena_id: UUID
    procesado_en: datetime


class ClasificacionBase(BaseSchema):
    """Schema base de Clasificación"""
    criterio_id: UUID
    valoracion: float = Field(..., ge=1, le=5)
    confianza: float = Field(0.0, ge=0, le=1)
    palabras_detectadas: Optional[List[str]] = None


class ClasificacionRead(ClasificacionBase):
    """Schema para leer Clasificación"""
    id: UUID
    resena_id: UUID
    procesado_en: datetime


class ResenaWithAnalysis(ResenaRead):
    """Reseña con análisis completo"""
    sentimiento: Optional[SentimientoRead] = None
    clasificaciones: List[ClasificacionRead] = []
