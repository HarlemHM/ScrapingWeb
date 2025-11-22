"""
Schemas para Hotel
"""
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr

from app.schemas.base import BaseSchema, TimestampSchema


class HotelBase(BaseSchema):
    """Schema base de Hotel"""
    nombre: str = Field(..., min_length=1, max_length=255)
    direccion: Optional[str] = Field(None, max_length=500)
    ciudad: Optional[str] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    sitio_web: Optional[str] = None
    latitud: Optional[float] = Field(None, ge=-90, le=90)
    longitud: Optional[float] = Field(None, ge=-180, le=180)
    activo: bool = True


class HotelCreate(HotelBase):
    """Schema para crear Hotel"""
    pass


class HotelUpdate(BaseSchema):
    """Schema para actualizar Hotel"""
    nombre: Optional[str] = Field(None, min_length=1, max_length=255)
    direccion: Optional[str] = Field(None, max_length=500)
    ciudad: Optional[str] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    sitio_web: Optional[str] = None
    latitud: Optional[float] = Field(None, ge=-90, le=90)
    longitud: Optional[float] = Field(None, ge=-180, le=180)
    activo: Optional[bool] = None


class HotelRead(HotelBase, TimestampSchema):
    """Schema para leer Hotel"""
    id: UUID
    
    
class HotelWithStats(HotelRead):
    """Hotel con estadísticas"""
    total_resenas: int = 0
    promedio_calificacion: Optional[float] = None
    ultimo_scraping: Optional[datetime] = None
