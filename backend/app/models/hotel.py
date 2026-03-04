"""
Modelo Hotel
"""
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Hotel(Base):
    """Establecimiento hotelero"""
    __tablename__ = "hoteles"
    __table_args__ = (
        sa.Index("ix_hoteles_nombre", "nombre"),
        sa.Index("ix_hoteles_ciudad", "ciudad"),
    )
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    nombre = sa.Column(sa.String(255), nullable=False)
    direccion = sa.Column(sa.Text, nullable=True)
    ciudad = sa.Column(sa.String(100), nullable=False, server_default="Barranquilla")
    telefono = sa.Column(sa.String(50), nullable=True)
    email = sa.Column(sa.String(255), nullable=True)
    sitio_web = sa.Column(sa.Text, nullable=True)
    descripcion = sa.Column(sa.Text, nullable=True)
    
    # Geolocalización
    latitud = sa.Column(sa.Float, nullable=True)
    longitud = sa.Column(sa.Float, nullable=True)
    
    # Metadata
    activo = sa.Column(sa.Boolean, nullable=False, server_default=sa.text("TRUE"))
    creado_en = sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()"))
    actualizado_en = sa.Column(sa.DateTime(timezone=True), nullable=True, onupdate=sa.text("now()"))
    
    # Relaciones
    plataformas = relationship("HotelPlataforma", back_populates="hotel", cascade="all, delete-orphan")
    indicadores = relationship("IndicadorPeriodo", back_populates="hotel", cascade="all, delete-orphan")
    resenas_destacadas = relationship("ResenaDestacada", back_populates="hotel", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Hotel(nombre='{self.nombre}', ciudad='{self.ciudad}')>"
