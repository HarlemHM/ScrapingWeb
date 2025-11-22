"""
CRUD para Hotel
"""
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.crud.base import CRUDBase
from app.models.hotel import Hotel
from app.models.hotel_plataforma import HotelPlataforma
from app.models.resena import Resena
from app.schemas.hotel import HotelCreate, HotelUpdate


class CRUDHotel(CRUDBase[Hotel, HotelCreate, HotelUpdate]):
    """CRUD para Hotel"""
    
    def get_by_nombre(self, db: Session, *, nombre: str) -> Optional[Hotel]:
        """Obtener hotel por nombre"""
        return db.query(Hotel).filter(Hotel.nombre == nombre).first()
    
    def get_active(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Hotel]:
        """Obtener hoteles activos"""
        return db.query(Hotel).filter(Hotel.activo == True).offset(skip).limit(limit).all()
    
    def get_by_ciudad(self, db: Session, *, ciudad: str, skip: int = 0, limit: int = 100) -> List[Hotel]:
        """Obtener hoteles por ciudad"""
        return (
            db.query(Hotel)
            .filter(Hotel.ciudad == ciudad, Hotel.activo == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_with_stats(self, db: Session, *, hotel_id: UUID) -> Optional[dict]:
        """Obtener hotel con estadísticas"""
        hotel = self.get(db, hotel_id)
        if not hotel:
            return None
        
        # Contar total de reseñas
        total_resenas = (
            db.query(func.count(Resena.id))
            .join(HotelPlataforma)
            .filter(HotelPlataforma.hotel_id == hotel_id)
            .scalar()
        )
        
        # Calcular promedio de calificación
        promedio_calificacion = (
            db.query(func.avg(Resena.puntuacion))
            .join(HotelPlataforma)
            .filter(HotelPlataforma.hotel_id == hotel_id)
            .scalar()
        )
        
        # Último scraping
        ultimo_scraping = (
            db.query(func.max(HotelPlataforma.ultimo_scraping))
            .filter(HotelPlataforma.hotel_id == hotel_id)
            .scalar()
        )
        
        return {
            "hotel": hotel,
            "total_resenas": total_resenas or 0,
            "promedio_calificacion": float(promedio_calificacion) if promedio_calificacion else None,
            "ultimo_scraping": ultimo_scraping,
        }


crud_hotel = CRUDHotel(Hotel)
