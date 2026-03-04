"""
Modelo HotelPlataforma - Relación entre Hotel y Plataforma
"""
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class HotelPlataforma(Base):
    """Relación entre hotel y plataforma de reseñas"""
    __tablename__ = "hotel_plataforma"
    __table_args__ = (
        sa.Index("ix_hotel_plataforma_hotel", "hotel_id"),
        sa.Index("ix_hotel_plataforma_plataforma", "plataforma_id"),
        sa.UniqueConstraint("hotel_id", "plataforma_id", name="uq_hotel_plataforma"),
    )
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    hotel_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("hoteles.id", ondelete="CASCADE"), nullable=False)
    plataforma_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("plataformas.id", ondelete="RESTRICT"), nullable=False)
    
    # URL del hotel en la plataforma
    url_hotel = sa.Column(sa.Text, nullable=True)
    identificador_externo = sa.Column(sa.String(255), nullable=True)  # ID del hotel en la plataforma
    
    # Metadata de scraping
    ultimo_scraping = sa.Column(sa.DateTime(timezone=True), nullable=True)
    total_resenas_extraidas = sa.Column(sa.Integer, nullable=False, server_default=sa.text("0"))
    
    # Metadata
    activo = sa.Column(sa.Boolean, nullable=False, server_default=sa.text("TRUE"))
    creado_en = sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()"))
    actualizado_en = sa.Column(sa.DateTime(timezone=True), nullable=True, onupdate=sa.text("now()"))
    
    # Relaciones
    hotel = relationship("Hotel", back_populates="plataformas")
    plataforma = relationship("Plataforma", back_populates="hoteles_plataformas")
    resenas = relationship("Resena", back_populates="hotel_plataforma", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<HotelPlataforma(hotel_id={self.hotel_id}, plataforma_id={self.plataforma_id})>"
