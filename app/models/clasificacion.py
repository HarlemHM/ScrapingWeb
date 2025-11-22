"""
Modelo Clasificación - Clasificación de reseñas por criterios
"""
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Clasificacion(Base):
    """Clasificación de una reseña según un criterio"""
    __tablename__ = "clasificaciones"
    __table_args__ = (
        sa.Index("ix_clasificaciones_resena", "resena_id"),
        sa.Index("ix_clasificaciones_criterio", "criterio_id"),
        sa.Index("ix_clasificaciones_valoracion", "valoracion"),
        sa.UniqueConstraint("resena_id", "criterio_id", name="uq_resena_criterio"),
    )
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    resena_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("resenas.id", ondelete="CASCADE"), nullable=False)
    criterio_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("criterios.id", ondelete="CASCADE"), nullable=False)
    
    # Valoración del criterio (1-5)
    valoracion = sa.Column(sa.Float, nullable=False)
    confianza = sa.Column(sa.Float, nullable=False, server_default=sa.text("0.0"))
    
    # Palabras clave detectadas en esta reseña para este criterio
    palabras_detectadas = sa.Column(sa.ARRAY(sa.String), nullable=True)
    
    # Metadata
    procesado_en = sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()"))
    
    # Relaciones
    resena = relationship("Resena", back_populates="clasificaciones")
    criterio = relationship("Criterio", back_populates="clasificaciones")
    
    def __repr__(self):
        return f"<Clasificacion(criterio_id={self.criterio_id}, valoracion={self.valoracion})>"
