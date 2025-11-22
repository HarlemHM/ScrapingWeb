"""
Schemas base y de uso común
"""
from datetime import datetime
from uuid import UUID
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    """Schema base con configuración común"""
    model_config = ConfigDict(from_attributes=True)


class TimestampSchema(BaseSchema):
    """Schema con timestamps"""
    creado_en: datetime
    actualizado_en: Optional[datetime] = None


class ResponseBase(BaseModel):
    """Response base para todas las respuestas"""
    success: bool = True
    message: str = "Operación exitosa"
    
    
class ErrorResponse(BaseModel):
    """Response para errores"""
    success: bool = False
    message: str
    detail: Optional[str] = None
    error_code: Optional[str] = None


class PaginatedResponse(BaseModel):
    """Response paginado genérico"""
    total: int
    page: int
    page_size: int
    total_pages: int
    items: list
