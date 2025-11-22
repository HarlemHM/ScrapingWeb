"""
Modelo Sentimiento - Análisis de sentimiento de reseñas
"""
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Sentimiento(Base):
    """Análisis de sentimiento de una reseña"""
    __tablename__ = "sentimientos"
    __table_args__ = (
        sa.Index("ix_sentimientos_tipo", "tipo_sentimiento"),
        sa.Index("ix_sentimientos_resena", "resena_id", unique=True),
    )
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    resena_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("resenas.id", ondelete="CASCADE"), nullable=False, unique=True)
    
    # Tipo de sentimiento
    tipo_sentimiento = sa.Column(sa.String(20), nullable=False)  # POSITIVO, NEGATIVO, NEUTRO
    
    # Scores de sentimiento (VADER o TextBlob)
    score_positivo = sa.Column(sa.Float, nullable=False, server_default=sa.text("0.0"))
    score_negativo = sa.Column(sa.Float, nullable=False, server_default=sa.text("0.0"))
    score_neutro = sa.Column(sa.Float, nullable=False, server_default=sa.text("0.0"))
    score_compuesto = sa.Column(sa.Float, nullable=False, server_default=sa.text("0.0"))  # -1 a 1
    
    # Confianza del análisis
    confianza = sa.Column(sa.Float, nullable=False, server_default=sa.text("0.0"))
    
    # Metadata
    procesado_en = sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()"))
    
    # Relaciones
    resena = relationship("Resena", back_populates="sentimiento")
    
    def __repr__(self):
        return f"<Sentimiento(tipo='{self.tipo_sentimiento}', score_compuesto={self.score_compuesto})>"
