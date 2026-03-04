"""
Modelo Plataforma
"""
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Plataforma(Base):
    """Plataforma de reseñas (Google, Booking, Airbnb, TripAdvisor)"""
    __tablename__ = "plataformas"
    __table_args__ = (
        sa.Index("ix_plataformas_codigo", "codigo", unique=True),
    )
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    codigo = sa.Column(sa.String(50), nullable=False, unique=True)  # GOOGLE, BOOKING, AIRBNB, TRIPADVISOR
    nombre = sa.Column(sa.String(100), nullable=False)
    descripcion = sa.Column(sa.Text, nullable=True)
    url_base = sa.Column(sa.Text, nullable=True)
    icono = sa.Column(sa.String(255), nullable=True)
    
    # Metadata
    activo = sa.Column(sa.Boolean, nullable=False, server_default=sa.text("TRUE"))
    creado_en = sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()"))
    
    # Relaciones
    hoteles_plataformas = relationship("HotelPlataforma", back_populates="plataforma")
    
    def __repr__(self):
        return f"<Plataforma(codigo='{self.codigo}', nombre='{self.nombre}')>"
