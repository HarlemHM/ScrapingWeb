"""
Modelo Criterio - Criterios de evaluación (Sostenibilidad, Calidad)
"""
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Criterio(Base):
    """Criterio de evaluación de reseñas"""
    __tablename__ = "criterios"
    __table_args__ = (
        sa.Index("ix_criterios_codigo", "codigo", unique=True),
    )
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    codigo = sa.Column(sa.String(50), nullable=False, unique=True)  # SOSTENIBILIDAD, CALIDAD
    nombre = sa.Column(sa.String(100), nullable=False)
    descripcion = sa.Column(sa.Text, nullable=True)
    peso = sa.Column(sa.Float, nullable=False, server_default=sa.text("1.0"))
    
    # Palabras clave asociadas al criterio
    palabras_clave = sa.Column(sa.ARRAY(sa.String), nullable=True)
    
    # Metadata
    activo = sa.Column(sa.Boolean, nullable=False, server_default=sa.text("TRUE"))
    creado_en = sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()"))
    
    # Relaciones
    clasificaciones = relationship("Clasificacion", back_populates="criterio")
    
    def __repr__(self):
        return f"<Criterio(codigo='{self.codigo}', nombre='{self.nombre}')>"
