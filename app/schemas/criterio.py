"""
Schemas para Criterios
"""
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class CriterioBase(BaseSchema):
    """Schema base de Criterio"""
    codigo: str = Field(..., min_length=1, max_length=50)
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = None
    peso: float = Field(1.0, ge=0)
    palabras_clave: Optional[List[str]] = None
    activo: bool = True


class CriterioCreate(CriterioBase):
    """Schema para crear Criterio"""
    pass


class CriterioRead(CriterioBase):
    """Schema para leer Criterio"""
    id: UUID
