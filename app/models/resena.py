"""
Modelo Reseña
"""
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Resena(Base):
    """Reseña de un hotel"""
    __tablename__ = "resenas"
    __table_args__ = (
        sa.Index("ix_resenas_hotel_plataforma", "hotel_plataforma_id"),
        sa.Index("ix_resenas_fecha_publicacion", "fecha_publicacion"),
        sa.Index("ix_resenas_puntuacion", "puntuacion"),
        sa.Index("ix_resenas_procesada", "procesada"),
        sa.Index("ix_resenas_hash", "hash_contenido"),
    )
    
    id = sa.Column(UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    hotel_plataforma_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("hotel_plataforma.id", ondelete="CASCADE"), nullable=False)
    
    # Datos del autor
    nombre_autor = sa.Column(sa.String(255), nullable=True)
    ubicacion_autor = sa.Column(sa.String(255), nullable=True)
    
    # Contenido de la reseña
    texto_positivo = sa.Column(sa.Text, nullable=True)  # Para Booking (separado)
    texto_negativo = sa.Column(sa.Text, nullable=True)  # Para Booking (separado)
    texto_completo = sa.Column(sa.Text, nullable=True)  # Para Google/Airbnb/TripAdvisor
    
    # Valoración
    puntuacion = sa.Column(sa.Float, nullable=True)  # Escala 1-5
    
    # Metadata de la reseña
    fecha_publicacion = sa.Column(sa.DateTime(timezone=True), nullable=True)
    tipo_estadia = sa.Column(sa.String(100), nullable=True)  # Familia, Pareja, Solo, Negocios
    titulo = sa.Column(sa.String(500), nullable=True)
    
    # Control de procesamiento
    procesada = sa.Column(sa.Boolean, nullable=False, server_default=sa.text("FALSE"))
    fecha_procesamiento = sa.Column(sa.DateTime(timezone=True), nullable=True)
    
    # Hash para evitar duplicados
    hash_contenido = sa.Column(sa.String(64), nullable=True, index=True)
    
    # Metadata
    creado_en = sa.Column(sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()"))
    
    # Relaciones
    hotel_plataforma = relationship("HotelPlataforma", back_populates="resenas")
    sentimiento = relationship("Sentimiento", back_populates="resena", uselist=False, cascade="all, delete-orphan")
    clasificaciones = relationship("Clasificacion", back_populates="resena", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Resena(id={self.id}, puntuacion={self.puntuacion})>"
