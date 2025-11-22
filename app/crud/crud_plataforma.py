"""
CRUD para Plataforma y HotelPlataforma
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.plataforma import Plataforma
from app.models.hotel_plataforma import HotelPlataforma
from app.schemas.plataforma import PlataformaCreate, HotelPlataformaCreate


class CRUDPlataforma(CRUDBase[Plataforma, PlataformaCreate, dict]):
    """CRUD para Plataforma"""
    
    def get_by_codigo(self, db: Session, *, codigo: str) -> Optional[Plataforma]:
        """Obtener plataforma por código"""
        return db.query(Plataforma).filter(Plataforma.codigo == codigo).first()
    
    def get_active(self, db: Session) -> List[Plataforma]:
        """Obtener plataformas activas"""
        return db.query(Plataforma).filter(Plataforma.activo == True).all()


class CRUDHotelPlataforma(CRUDBase[HotelPlataforma, HotelPlataformaCreate, dict]):
    """CRUD para HotelPlataforma"""
    
    def get_by_hotel_and_plataforma(
        self, db: Session, *, hotel_id: UUID, plataforma_id: UUID
    ) -> Optional[HotelPlataforma]:
        """Obtener relación hotel-plataforma"""
        return (
            db.query(HotelPlataforma)
            .filter(
                HotelPlataforma.hotel_id == hotel_id,
                HotelPlataforma.plataforma_id == plataforma_id
            )
            .first()
        )
    
    def get_by_hotel(self, db: Session, *, hotel_id: UUID) -> List[HotelPlataforma]:
        """Obtener todas las plataformas de un hotel"""
        return (
            db.query(HotelPlataforma)
            .filter(HotelPlataforma.hotel_id == hotel_id, HotelPlataforma.activo == True)
            .all()
        )
    
    def update_scraping_stats(
        self,
        db: Session,
        *,
        hotel_plataforma_id: UUID,
        total_extraidas: int
    ) -> HotelPlataforma:
        """Actualizar estadísticas de scraping"""
        hp = self.get(db, hotel_plataforma_id)
        if hp:
            hp.ultimo_scraping = datetime.utcnow()
            hp.total_resenas_extraidas += total_extraidas
            db.commit()
            db.refresh(hp)
        return hp


crud_plataforma = CRUDPlataforma(Plataforma)
crud_hotel_plataforma = CRUDHotelPlataforma(HotelPlataforma)
