"""
Modelo ResenaDestacada - Reseñas destacadas para visualización
"""
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class ResenaDestacada(Base):
    """Reseñas destacadas de un hotel"""
    __tablename__ = "resenas_destacadas"
    __table_args__ = (
        sa.Index("ix_resenas_destacadas_hotel", "hotel_id"),
        sa.Index("ix_resenas_destacadas_tipo", "tipo"),
    )
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    hotel_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("hoteles.id", ondelete="CASCADE"), nullable=False)
    resena_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("resenas.id", ondelete="CASCADE"), nullable=False)
    
    # Tipo de destacado
    tipo = sa.Column(sa.String(50), nullable=False)  # ULTIMA, MAS_POSITIVA, MAS_NEGATIVA
    
    # Período de análisis
    periodo_inicio = sa.Column(sa.DateTime(timezone=True), nullable=True)
    periodo_fin = sa.Column(sa.DateTime(timezone=True), nullable=True)
    
    # Metadata
    creado_en = sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()"))
    
    # Relaciones
    hotel = relationship("Hotel", back_populates="resenas_destacadas")
    
    def __repr__(self):
        return f"<ResenaDestacada(tipo='{self.tipo}', hotel_id={self.hotel_id})>"
