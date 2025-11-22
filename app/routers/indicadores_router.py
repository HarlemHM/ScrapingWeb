"""
Router de Indicadores - Análisis Cuantitativo y Visualización Comparativa
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud import crud_hotel
from app.schemas.indicador import IndicadoresResumen
from app.services.indicadores_service import indicadores_service

router = APIRouter()


@router.get("/resumen", response_model=dict)
def obtener_resumen_global(
    fecha_inicio: Optional[datetime] = Query(None, description="Fecha desde"),
    fecha_fin: Optional[datetime] = Query(None, description="Fecha hasta"),
    sostenibilidad_min: Optional[float] = Query(None, ge=1, le=5, description="Sostenibilidad mínima"),
    calidad_min: Optional[float] = Query(None, ge=1, le=5, description="Calidad mínima"),
    db: Session = Depends(get_db)
):
    """
    Obtener resumen global de todos los hoteles.
    Usado para los 4 cards principales del Análisis Cuantitativo:
    - Total Hoteles
    - Promedio Sostenibilidad
    - Promedio Calidad  
    - Total Reseñas
    """
    from app.models.hotel import Hotel
    from app.models.resena import Resena
    from app.models.hotel_plataforma import HotelPlataforma
    from app.models.clasificacion import Clasificacion
    from app.crud import crud_criterio
    from sqlalchemy import func, and_
    
    # Total de hoteles activos
    total_hoteles = db.query(func.count(Hotel.id)).filter(Hotel.activo == True).scalar()
    
    # Query base de reseñas
    query = (
        db.query(Resena)
        .join(HotelPlataforma)
        .join(Hotel)
        .filter(
            and_(
                Hotel.activo == True,
                Resena.procesada == True
            )
        )
    )
    
    if fecha_inicio:
        query = query.filter(Resena.fecha_publicacion >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Resena.fecha_publicacion <= fecha_fin)
    
    # Total reseñas
    total_resenas = query.count()
    
    # Obtener IDs de reseñas
    resena_ids = [r.id for r in query.all()]
    
    if not resena_ids:
        return {
            "total_hoteles": total_hoteles,
            "promedio_sostenibilidad": 0.0,
            "promedio_calidad": 0.0,
            "total_resenas": 0
        }
    
    # Criterios
    criterio_sost = crud_criterio.get_by_codigo(db, codigo="SOSTENIBILIDAD")
    criterio_cal = crud_criterio.get_by_codigo(db, codigo="CALIDAD")
    
    promedio_sostenibilidad = 0.0
    promedio_calidad = 0.0
    
    if criterio_sost:
        avg_sost = (
            db.query(func.avg(Clasificacion.valoracion))
            .filter(
                and_(
                    Clasificacion.resena_id.in_(resena_ids),
                    Clasificacion.criterio_id == criterio_sost.id
                )
            )
            .scalar()
        )
        promedio_sostenibilidad = round(float(avg_sost), 1) if avg_sost else 0.0
    
    if criterio_cal:
        avg_cal = (
            db.query(func.avg(Clasificacion.valoracion))
            .filter(
                and_(
                    Clasificacion.resena_id.in_(resena_ids),
                    Clasificacion.criterio_id == criterio_cal.id
                )
            )
            .scalar()
        )
        promedio_calidad = round(float(avg_cal), 1) if avg_cal else 0.0
    
    # Aplicar filtros de sostenibilidad y calidad si se especifican
    # (esto filtraría los hoteles que cumplen los criterios mínimos)
    
    return {
        "total_hoteles": total_hoteles,
        "promedio_sostenibilidad": promedio_sostenibilidad,
        "promedio_calidad": promedio_calidad,
        "total_resenas": total_resenas
    }


@router.get("/tabla-hoteles", response_model=List[dict])
def obtener_tabla_hoteles(
    fecha_inicio: Optional[datetime] = Query(None),
    fecha_fin: Optional[datetime] = Query(None),
    sostenibilidad_min: Optional[float] = Query(None, ge=1, le=5),
    calidad_min: Optional[float] = Query(None, ge=1, le=5),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtener tabla de hoteles con indicadores.
    Usado para la tabla principal del Análisis Cuantitativo con:
    - Hotel, Sostenibilidad, Calidad, Reseñas, Sentimiento, Plataforma
    """
    from app.models.hotel import Hotel
    from app.models.resena import Resena
    from app.models.sentimiento import Sentimiento
    from app.models.hotel_plataforma import HotelPlataforma
    from app.models.plataforma import Plataforma
    from app.models.clasificacion import Clasificacion
    from app.crud import crud_criterio
    from sqlalchemy import func, and_, desc
    
    hoteles = crud_hotel.get_active(db, skip=skip, limit=limit)
    
    criterio_sost = crud_criterio.get_by_codigo(db, codigo="SOSTENIBILIDAD")
    criterio_cal = crud_criterio.get_by_codigo(db, codigo="CALIDAD")
    
    resultado = []
    
    for hotel in hoteles:
        # Query de reseñas del hotel
        query_resenas = (
            db.query(Resena)
            .join(HotelPlataforma)
            .filter(
                and_(
                    HotelPlataforma.hotel_id == hotel.id,
                    Resena.procesada == True
                )
            )
        )
        
        if fecha_inicio:
            query_resenas = query_resenas.filter(Resena.fecha_publicacion >= fecha_inicio)
        if fecha_fin:
            query_resenas = query_resenas.filter(Resena.fecha_publicacion <= fecha_fin)
        
        resenas = query_resenas.all()
        
        if not resenas:
            continue
        
        resena_ids = [r.id for r in resenas]
        total_resenas = len(resenas)
        
        # Sostenibilidad
        sost = 0.0
        if criterio_sost:
            avg_sost = (
                db.query(func.avg(Clasificacion.valoracion))
                .filter(
                    and_(
                        Clasificacion.resena_id.in_(resena_ids),
                        Clasificacion.criterio_id == criterio_sost.id
                    )
                )
                .scalar()
            )
            sost = round(float(avg_sost), 1) if avg_sost else 0.0
        
        # Calidad
        cal = 0.0
        if criterio_cal:
            avg_cal = (
                db.query(func.avg(Clasificacion.valoracion))
                .filter(
                    and_(
                        Clasificacion.resena_id.in_(resena_ids),
                        Clasificacion.criterio_id == criterio_cal.id
                    )
                )
                .scalar()
            )
            cal = round(float(avg_cal), 1) if avg_cal else 0.0
        
        # Aplicar filtros mínimos
        if sostenibilidad_min and sost < sostenibilidad_min:
            continue
        if calidad_min and cal < calidad_min:
            continue
        
        # Sentimiento predominante
        sentimientos = (
            db.query(Sentimiento.tipo_sentimiento, func.count(Sentimiento.id))
            .filter(Sentimiento.resena_id.in_(resena_ids))
            .group_by(Sentimiento.tipo_sentimiento)
            .order_by(desc(func.count(Sentimiento.id)))
            .first()
        )
        
        sentimiento_predominante = sentimientos[0] if sentimientos else "NEUTRO"
        
        # Plataforma con más reseñas
        plataforma_top = (
            db.query(Plataforma.codigo, func.count(Resena.id))
            .join(HotelPlataforma, HotelPlataforma.plataforma_id == Plataforma.id)
            .join(Resena, Resena.hotel_plataforma_id == HotelPlataforma.id)
            .filter(
                and_(
                    HotelPlataforma.hotel_id == hotel.id,
                    Resena.id.in_(resena_ids)
                )
            )
            .group_by(Plataforma.codigo)
            .order_by(desc(func.count(Resena.id)))
            .first()
        )
        
        plataforma_nombre = plataforma_top[0].lower() if plataforma_top else "google"
        
        resultado.append({
            "hotel_id": str(hotel.id),
            "hotel_nombre": hotel.nombre,
            "sostenibilidad": sost,
            "calidad": cal,
            "total_resenas": total_resenas,
            "sentimiento": sentimiento_predominante.lower(),
            "plataforma": plataforma_nombre
        })
    
    return resultado


@router.get("/distribucion-plataformas", response_model=List[dict])
def obtener_distribucion_plataformas(
    fecha_inicio: Optional[datetime] = Query(None),
    fecha_fin: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Distribución de reseñas por plataforma.
    Usado para el gráfico de barras en Visualización Comparativa.
    """
    distribuciones = indicadores_service.obtener_distribucion_plataformas(
        db, fecha_inicio, fecha_fin
    )
    return distribuciones


@router.get("/distribucion-sentimientos", response_model=dict)
def obtener_distribucion_sentimientos(
    fecha_inicio: Optional[datetime] = Query(None),
    fecha_fin: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Distribución de sentimientos (positivos, negativos, neutros).
    Usado para el gráfico de barras horizontales en Visualización Comparativa.
    """
    from app.models.resena import Resena
    from app.models.sentimiento import Sentimiento
    from sqlalchemy import func, and_
    
    query = db.query(Resena).filter(Resena.procesada == True)
    
    if fecha_inicio:
        query = query.filter(Resena.fecha_publicacion >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Resena.fecha_publicacion <= fecha_fin)
    
    resena_ids = [r.id for r in query.all()]
    
    if not resena_ids:
        return {"positivos": 0, "negativos": 0, "neutros": 0}
    
    sentimientos = (
        db.query(Sentimiento.tipo_sentimiento, func.count(Sentimiento.id))
        .filter(Sentimiento.resena_id.in_(resena_ids))
        .group_by(Sentimiento.tipo_sentimiento)
        .all()
    )
    
    resultado = {"positivos": 0, "negativos": 0, "neutros": 0}
    
    for tipo, count in sentimientos:
        if tipo == "POSITIVO":
            resultado["positivos"] = count
        elif tipo == "NEGATIVO":
            resultado["negativos"] = count
        elif tipo == "NEUTRO":
            resultado["neutros"] = count
    
    return resultado


@router.get("/comparacion-hoteles", response_model=List[dict])
def obtener_comparacion_hoteles(
    fecha_inicio: Optional[datetime] = Query(None),
    fecha_fin: Optional[datetime] = Query(None),
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Comparación de sostenibilidad y calidad por hotel.
    Usado para el gráfico de barras agrupadas en Visualización Comparativa.
    """
    from app.models.hotel import Hotel
    from app.models.resena import Resena
    from app.models.hotel_plataforma import HotelPlataforma
    from app.models.clasificacion import Clasificacion
    from app.crud import crud_criterio
    from sqlalchemy import func, and_
    
    hoteles = crud_hotel.get_active(db, limit=limit)
    
    criterio_sost = crud_criterio.get_by_codigo(db, codigo="SOSTENIBILIDAD")
    criterio_cal = crud_criterio.get_by_codigo(db, codigo="CALIDAD")
    
    resultado = []
    
    for hotel in hoteles:
        query_resenas = (
            db.query(Resena)
            .join(HotelPlataforma)
            .filter(
                and_(
                    HotelPlataforma.hotel_id == hotel.id,
                    Resena.procesada == True
                )
            )
        )
        
        if fecha_inicio:
            query_resenas = query_resenas.filter(Resena.fecha_publicacion >= fecha_inicio)
        if fecha_fin:
            query_resenas = query_resenas.filter(Resena.fecha_publicacion <= fecha_fin)
        
        resenas = query_resenas.all()
        
        if not resenas:
            continue
        
        resena_ids = [r.id for r in resenas]
        
        sost = 0.0
        cal = 0.0
        
        if criterio_sost:
            avg_sost = (
                db.query(func.avg(Clasificacion.valoracion))
                .filter(
                    and_(
                        Clasificacion.resena_id.in_(resena_ids),
                        Clasificacion.criterio_id == criterio_sost.id
                    )
                )
                .scalar()
            )
            sost = round(float(avg_sost), 1) if avg_sost else 0.0
        
        if criterio_cal:
            avg_cal = (
                db.query(func.avg(Clasificacion.valoracion))
                .filter(
                    and_(
                        Clasificacion.resena_id.in_(resena_ids),
                        Clasificacion.criterio_id == criterio_cal.id
                    )
                )
                .scalar()
            )
            cal = round(float(avg_cal), 1) if avg_cal else 0.0
        
        resultado.append({
            "hotel": hotel.nombre,
            "sostenibilidad": sost,
            "calidad": cal
        })
    
    return resultado


@router.get("/{hotel_id}/resumen", response_model=IndicadoresResumen)
def obtener_resumen_hotel(
    hotel_id: UUID,
    fecha_inicio: Optional[datetime] = Query(None),
    fecha_fin: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):
    """Obtener resumen de indicadores de un hotel específico"""
    hotel = crud_hotel.get(db, hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel no encontrado")
    
    resumen = indicadores_service.obtener_resumen_hotel(
        db, hotel_id, fecha_inicio, fecha_fin
    )
    
    return resumen
