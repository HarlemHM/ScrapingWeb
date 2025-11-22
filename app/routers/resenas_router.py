"""
Router de Reseñas
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud import crud_resena, crud_hotel_plataforma
from app.schemas.resena import ResenaRead, ResenaWithAnalysis
from app.schemas.base import PaginatedResponse

router = APIRouter()


@router.get("/{hotel_id}", response_model=List[ResenaWithAnalysis])
def listar_resenas_hotel(
    hotel_id: UUID,
    skip: int = 0,
    limit: int = 100,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    plataforma_codigo: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Listar reseñas de un hotel con filtros.
    Usado por el frontend para Análisis Cualitativo con filtros de fecha.
    """
    from app.crud import crud_plataforma, crud_hotel
    from app.models.resena import Resena
    from app.models.hotel_plataforma import HotelPlataforma
    from sqlalchemy import and_
    
    # Verificar que el hotel existe
    hotel = crud_hotel.get(db, hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel no encontrado")
    
    # Construir query base
    query = (
        db.query(Resena)
        .join(HotelPlataforma)
        .filter(
            and_(
                HotelPlataforma.hotel_id == hotel_id,
                Resena.procesada == True
            )
        )
    )
    
    # Aplicar filtros de fecha
    if fecha_inicio:
        query = query.filter(Resena.fecha_publicacion >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Resena.fecha_publicacion <= fecha_fin)
    
    # Filtro por plataforma
    if plataforma_codigo:
        from app.models.plataforma import Plataforma
        plataforma = crud_plataforma.get_by_codigo(db, codigo=plataforma_codigo)
        if plataforma:
            query = query.filter(HotelPlataforma.plataforma_id == plataforma.id)
    
    # Obtener reseñas
    resenas = query.order_by(Resena.fecha_publicacion.desc()).offset(skip).limit(limit).all()
    
    # Cargar relaciones manualmente
    result = []
    for resena in resenas:
        resena_dict = ResenaRead.model_validate(resena).model_dump()
        
        # Cargar sentimiento
        sentimiento = crud_resena.get(db, resena.id)
        if hasattr(sentimiento, 'sentimiento') and sentimiento.sentimiento:
            from app.schemas.resena import SentimientoRead
            resena_dict['sentimiento'] = SentimientoRead.model_validate(sentimiento.sentimiento)
        
        # Cargar clasificaciones
        from app.crud import crud_clasificacion
        clasificaciones = crud_clasificacion.get_by_resena(db, resena_id=resena.id)
        from app.schemas.resena import ClasificacionRead
        resena_dict['clasificaciones'] = [
            ClasificacionRead.model_validate(c) for c in clasificaciones
        ]
        
        result.append(resena_dict)
    
    return result


@router.get("/destacadas/{hotel_id}", response_model=dict)
def obtener_resenas_destacadas(
    hotel_id: UUID,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    Obtener reseñas destacadas (últimas, más positivas, más negativas).
    Usado para Análisis Cualitativo.
    """
    from app.services.indicadores_service import indicadores_service
    
    destacadas = indicadores_service.obtener_resenas_destacadas(
        db, hotel_id, fecha_inicio, fecha_fin
    )
    
    resultado = {
        "ultima": None,
        "mas_positiva": None,
        "mas_negativa": None
    }
    
    if destacadas.get("ultima"):
        resultado["ultima"] = ResenaRead.model_validate(destacadas["ultima"])
    
    if destacadas.get("mas_positiva"):
        resultado["mas_positiva"] = ResenaRead.model_validate(destacadas["mas_positiva"])
    
    if destacadas.get("mas_negativa"):
        resultado["mas_negativa"] = ResenaRead.model_validate(destacadas["mas_negativa"])
    
    return resultado
