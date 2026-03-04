"""
Schemas para Plataforma
"""
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.base import BaseSchema


class PlataformaBase(BaseSchema):
    """Schema base de Plataforma"""
    codigo: str = Field(..., min_length=1, max_length=50)
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = None
    url_base: Optional[str] = None
    icono: Optional[str] = Field(None, max_length=255)
    activo: bool = True


class PlataformaCreate(PlataformaBase):
    """Schema para crear Plataforma"""
    pass


class PlataformaRead(PlataformaBase):
    """Schema para leer Plataforma"""
    id: UUID
    
    
class HotelPlataformaBase(BaseSchema):
    """Schema base de HotelPlataforma"""
    hotel_id: UUID
    plataforma_id: UUID
    url_hotel: Optional[str] = None
    identificador_externo: Optional[str] = Field(None, max_length=255)
    activo: bool = True


class HotelPlataformaCreate(HotelPlataformaBase):
    """Schema para crear HotelPlataforma"""
    pass


class HotelPlataformaRead(HotelPlataformaBase):
    """Schema para leer HotelPlataforma"""
    id: UUID
    ultimo_scraping: Optional[str] = None
    total_resenas_extraidas: int = 0
    
    
class HotelPlataformaWithInfo(HotelPlataformaRead):
    """HotelPlataforma con información de plataforma"""
    plataforma: PlataformaRead
