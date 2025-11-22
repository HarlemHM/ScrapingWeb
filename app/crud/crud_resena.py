"""
CRUD para Reseña, Sentimiento y Clasificación
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime
import hashlib

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc

from app.crud.base import CRUDBase
from app.models.resena import Resena
from app.models.sentimiento import Sentimiento
from app.models.clasificacion import Clasificacion
from app.schemas.resena import ResenaCreate, SentimientoBase, ClasificacionBase


class CRUDResena(CRUDBase[Resena, ResenaCreate, dict]):
    """CRUD para Reseña"""
    
    def create_with_hash(self, db: Session, *, obj_in: ResenaCreate) -> Resena:
        """Crear reseña con hash para evitar duplicados"""
        # Generar hash del contenido
        texto_para_hash = ""
        if obj_in.texto_completo:
            texto_para_hash = obj_in.texto_completo
        elif obj_in.texto_positivo or obj_in.texto_negativo:
            texto_para_hash = f"{obj_in.texto_positivo or ''}{obj_in.texto_negativo or ''}"
        
        hash_contenido = hashlib.sha256(texto_para_hash.encode()).hexdigest()
        
        # Verificar si ya existe
        existing = self.get_by_hash(db, hash_contenido=hash_contenido)
        if existing:
            return existing
        
        # Crear nueva reseña
        resena_data = obj_in.model_dump()
        resena_data["hash_contenido"] = hash_contenido
        db_obj = Resena(**resena_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_hash(self, db: Session, *, hash_contenido: str) -> Optional[Resena]:
        """Obtener reseña por hash"""
        return db.query(Resena).filter(Resena.hash_contenido == hash_contenido).first()
    
    def get_by_hotel_plataforma(
        self, db: Session, *, hotel_plataforma_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Resena]:
        """Obtener reseñas de un hotel en una plataforma"""
        return (
            db.query(Resena)
            .filter(Resena.hotel_plataforma_id == hotel_plataforma_id)
            .order_by(desc(Resena.fecha_publicacion))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_pending_processing(self, db: Session, *, limit: int = 100) -> List[Resena]:
        """Obtener reseñas pendientes de procesar"""
        return (
            db.query(Resena)
            .filter(Resena.procesada == False)
            .limit(limit)
            .all()
        )
    
    def mark_as_processed(self, db: Session, *, resena_id: UUID) -> Resena:
        """Marcar reseña como procesada"""
        resena = self.get(db, resena_id)
        if resena:
            resena.procesada = True
            resena.fecha_procesamiento = datetime.utcnow()
            db.commit()
            db.refresh(resena)
        return resena


class CRUDSentimiento(CRUDBase[Sentimiento, SentimientoBase, dict]):
    """CRUD para Sentimiento"""
    
    def get_by_resena(self, db: Session, *, resena_id: UUID) -> Optional[Sentimiento]:
        """Obtener sentimiento de una reseña"""
        return db.query(Sentimiento).filter(Sentimiento.resena_id == resena_id).first()


class CRUDClasificacion(CRUDBase[Clasificacion, ClasificacionBase, dict]):
    """CRUD para Clasificación"""
    
    def get_by_resena(self, db: Session, *, resena_id: UUID) -> List[Clasificacion]:
        """Obtener clasificaciones de una reseña"""
        return db.query(Clasificacion).filter(Clasificacion.resena_id == resena_id).all()
    
    def get_by_resena_and_criterio(
        self, db: Session, *, resena_id: UUID, criterio_id: UUID
    ) -> Optional[Clasificacion]:
        """Obtener clasificación específica"""
        return (
            db.query(Clasificacion)
            .filter(
                Clasificacion.resena_id == resena_id,
                Clasificacion.criterio_id == criterio_id
            )
            .first()
        )


crud_resena = CRUDResena(Resena)
crud_sentimiento = CRUDSentimiento(Sentimiento)
crud_clasificacion = CRUDClasificacion(Clasificacion)
