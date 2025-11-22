"""
Schemas para Indicadores
"""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class IndicadorPeriodoBase(BaseSchema):
    """Schema base de IndicadorPeriodo"""
    hotel_id: UUID
    periodo_inicio: datetime
    periodo_fin: datetime
    total_resenas: int = 0
    promedio_sostenibilidad: Optional[float] = Field(None, ge=1, le=5)
    promedio_calidad: Optional[float] = Field(None, ge=1, le=5)
    promedio_general: Optional[float] = Field(None, ge=1, le=5)
    total_positivas: int = 0
    total_negativas: int = 0
    total_neutras: int = 0


class IndicadorPeriodoRead(IndicadorPeriodoBase):
    """Schema para leer IndicadorPeriodo"""
    id: UUID
    calculado_en: datetime
    actualizado_en: Optional[datetime] = None


class IndicadoresResumen(BaseSchema):
    """Resumen de indicadores"""
    total_resenas: int
    promedio_sostenibilidad: float
    promedio_calidad: float
    promedio_general: float
    porcentaje_positivas: float
    porcentaje_negativas: float
    porcentaje_neutras: float


class ResenaDestacadaRead(BaseSchema):
    """Schema para ResenaDestacada"""
    id: UUID
    hotel_id: UUID
    resena_id: UUID
    tipo: str  # ULTIMA, MAS_POSITIVA, MAS_NEGATIVA
    periodo_inicio: Optional[datetime] = None
    periodo_fin: Optional[datetime] = None
