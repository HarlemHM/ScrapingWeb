"""
Modelo IndicadorPeriodo - Indicadores agregados por hotel y período
"""
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class IndicadorPeriodo(Base):
    """Indicadores agregados de un hotel en un período"""
    __tablename__ = "indicadores_periodo"
    __table_args__ = (
        sa.Index("ix_indicadores_hotel", "hotel_id"),
        sa.Index("ix_indicadores_periodo", "periodo_inicio", "periodo_fin"),
        sa.UniqueConstraint("hotel_id", "periodo_inicio", "periodo_fin", name="uq_hotel_periodo"),
    )
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    hotel_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("hoteles.id", ondelete="CASCADE"), nullable=False)
    
    # Período
    periodo_inicio = sa.Column(sa.DateTime(timezone=True), nullable=False)
    periodo_fin = sa.Column(sa.DateTime(timezone=True), nullable=False)
    
    # Indicadores cuantitativos
    total_resenas = sa.Column(sa.Integer, nullable=False, server_default=sa.text("0"))
    promedio_sostenibilidad = sa.Column(sa.Float, nullable=True)
    promedio_calidad = sa.Column(sa.Float, nullable=True)
    promedio_general = sa.Column(sa.Float, nullable=True)
    
    # Distribución de sentimientos
    total_positivas = sa.Column(sa.Integer, nullable=False, server_default=sa.text("0"))
    total_negativas = sa.Column(sa.Integer, nullable=False, server_default=sa.text("0"))
    total_neutras = sa.Column(sa.Integer, nullable=False, server_default=sa.text("0"))
    
    # Metadata
    calculado_en = sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()"))
    actualizado_en = sa.Column(sa.DateTime(timezone=True), nullable=True, onupdate=sa.text("now()"))
    
    # Relaciones
    hotel = relationship("Hotel", back_populates="indicadores")
    
    def __repr__(self):
        return f"<IndicadorPeriodo(hotel_id={self.hotel_id}, total_resenas={self.total_resenas})>"
