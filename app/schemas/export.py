"""
Schemas para Exportación
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema, ResponseBase


class ExportRequest(BaseSchema):
    """Request para exportar datos"""
    hotel_id: UUID
    formato: str = Field(..., pattern="^(PDF|CSV)$")
    periodo_inicio: Optional[datetime] = None
    periodo_fin: Optional[datetime] = None
    incluir_graficos: bool = True
    incluir_resenas: bool = True


class ExportResponse(ResponseBase):
    """Response de exportación"""
    job_id: str
    message: str = "Exportación iniciada correctamente"


class ExportStatus(BaseSchema):
    """Estado de una exportación"""
    job_id: str
    status: str  # PENDING, STARTED, SUCCESS, FAILURE
    archivo_url: Optional[str] = None
    error: Optional[str] = None
