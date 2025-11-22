"""
Servicio de Indicadores - Cálculo de métricas y estadísticas
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.crud import (
    crud_hotel, crud_indicador_periodo, crud_resena_destacada,
    crud_resena, crud_sentimiento, crud_clasificacion, crud_criterio
)
from app.models.resena import Resena
from app.models.sentimiento import Sentimiento
from app.models.clasificacion import Clasificacion
from app.models.hotel_plataforma import HotelPlataforma
from app.schemas.indicador import IndicadorPeriodoBase, IndicadoresResumen


class IndicadoresService:
    """Servicio de cálculo de indicadores y métricas"""
    
    def calcular_indicadores_periodo(
        self,
        db: Session,
        hotel_id: UUID,
        fecha_inicio: datetime,
        fecha_fin: datetime
    ) -> Dict[str, any]:
        """Calcular indicadores de un hotel en un período"""
        
        # Obtener reseñas del período
        resenas = (
            db.query(Resena)
            .join(HotelPlataforma)
            .filter(
                and_(
                    HotelPlataforma.hotel_id == hotel_id,
                    Resena.fecha_publicacion >= fecha_inicio,
                    Resena.fecha_publicacion <= fecha_fin,
                    Resena.procesada == True
                )
            )
            .all()
        )
        
        if not resenas:
            return None
        
        total_resenas = len(resenas)
        resena_ids = [r.id for r in resenas]
        
        # Promedio general de puntuaciones
        promedio_general = sum(r.puntuacion for r in resenas if r.puntuacion) / total_resenas
        
        # Contar sentimientos
        sentimientos = (
            db.query(Sentimiento.tipo_sentimiento, func.count(Sentimiento.id))
            .filter(Sentimiento.resena_id.in_(resena_ids))
            .group_by(Sentimiento.tipo_sentimiento)
            .all()
        )
        
        total_positivas = 0
        total_negativas = 0
        total_neutras = 0
        
        for tipo, count in sentimientos:
            if tipo == "POSITIVO":
                total_positivas = count
            elif tipo == "NEGATIVO":
                total_negativas = count
            elif tipo == "NEUTRO":
                total_neutras = count
        
        # Promedio por criterio
        criterios = crud_criterio.get_active(db)
        promedio_sostenibilidad = None
        promedio_calidad = None
        
        for criterio in criterios:
            avg_valoracion = (
                db.query(func.avg(Clasificacion.valoracion))
                .filter(
                    and_(
                        Clasificacion.resena_id.in_(resena_ids),
                        Clasificacion.criterio_id == criterio.id
                    )
                )
                .scalar()
            )
            
            if criterio.codigo == "SOSTENIBILIDAD":
                promedio_sostenibilidad = float(avg_valoracion) if avg_valoracion else None
            elif criterio.codigo == "CALIDAD":
                promedio_calidad = float(avg_valoracion) if avg_valoracion else None
        
        # Crear o actualizar indicador
        indicador_data = IndicadorPeriodoBase(
            hotel_id=hotel_id,
            periodo_inicio=fecha_inicio,
            periodo_fin=fecha_fin,
            total_resenas=total_resenas,
            promedio_sostenibilidad=promedio_sostenibilidad,
            promedio_calidad=promedio_calidad,
            promedio_general=round(promedio_general, 2),
            total_positivas=total_positivas,
            total_negativas=total_negativas,
            total_neutras=total_neutras
        )
        
        # Verificar si ya existe
        existing = crud_indicador_periodo.get_by_hotel_and_periodo(
            db,
            hotel_id=hotel_id,
            periodo_inicio=fecha_inicio,
            periodo_fin=fecha_fin
        )
        
        if existing:
            return crud_indicador_periodo.update(
                db, db_obj=existing, obj_in=indicador_data.model_dump()
            )
        else:
            return crud_indicador_periodo.create(db, obj_in=indicador_data)
    
    def obtener_resumen_hotel(
        self,
        db: Session,
        hotel_id: UUID,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None
    ) -> IndicadoresResumen:
        """Obtener resumen de indicadores de un hotel"""
        
        # Filtros de fecha
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
        
        if fecha_inicio:
            query = query.filter(Resena.fecha_publicacion >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Resena.fecha_publicacion <= fecha_fin)
        
        resenas = query.all()
        
        if not resenas:
            return IndicadoresResumen(
                total_resenas=0,
                promedio_sostenibilidad=0.0,
                promedio_calidad=0.0,
                promedio_general=0.0,
                porcentaje_positivas=0.0,
                porcentaje_negativas=0.0,
                porcentaje_neutras=0.0
            )
        
        total_resenas = len(resenas)
        resena_ids = [r.id for r in resenas]
        
        # Promedio general
        promedio_general = sum(r.puntuacion for r in resenas if r.puntuacion) / total_resenas
        
        # Sentimientos
        sentimientos = (
            db.query(Sentimiento.tipo_sentimiento, func.count(Sentimiento.id))
            .filter(Sentimiento.resena_id.in_(resena_ids))
            .group_by(Sentimiento.tipo_sentimiento)
            .all()
        )
        
        sent_counts = {tipo: count for tipo, count in sentimientos}
        total_positivas = sent_counts.get("POSITIVO", 0)
        total_negativas = sent_counts.get("NEGATIVO", 0)
        total_neutras = sent_counts.get("NEUTRO", 0)
        
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
            promedio_sostenibilidad = float(avg_sost) if avg_sost else 0.0
        
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
            promedio_calidad = float(avg_cal) if avg_cal else 0.0
        
        return IndicadoresResumen(
            total_resenas=total_resenas,
            promedio_sostenibilidad=round(promedio_sostenibilidad, 2),
            promedio_calidad=round(promedio_calidad, 2),
            promedio_general=round(promedio_general, 2),
            porcentaje_positivas=round((total_positivas / total_resenas) * 100, 2),
            porcentaje_negativas=round((total_negativas / total_resenas) * 100, 2),
            porcentaje_neutras=round((total_neutras / total_resenas) * 100, 2)
        )
    
    def obtener_distribucion_plataformas(
        self,
        db: Session,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None
    ) -> List[Dict[str, any]]:
        """Obtener distribución de reseñas por plataforma"""
        
        from app.models.plataforma import Plataforma
        
        query = (
            db.query(
                Plataforma.codigo,
                Plataforma.nombre,
                func.count(Resena.id).label('total')
            )
            .join(HotelPlataforma, HotelPlataforma.plataforma_id == Plataforma.id)
            .join(Resena, Resena.hotel_plataforma_id == HotelPlataforma.id)
            .filter(Resena.procesada == True)
        )
        
        if fecha_inicio:
            query = query.filter(Resena.fecha_publicacion >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Resena.fecha_publicacion <= fecha_fin)
        
        query = query.group_by(Plataforma.codigo, Plataforma.nombre)
        
        resultados = query.all()
        
        return [
            {
                "plataforma": codigo,
                "nombre": nombre,
                "total": total
            }
            for codigo, nombre, total in resultados
        ]
    
    def obtener_resenas_destacadas(
        self,
        db: Session,
        hotel_id: UUID,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None
    ) -> Dict[str, any]:
        """Obtener reseñas destacadas (última, más positiva, más negativa)"""
        
        query = (
            db.query(Resena)
            .join(HotelPlataforma)
            .join(Sentimiento, Sentimiento.resena_id == Resena.id)
            .filter(
                and_(
                    HotelPlataforma.hotel_id == hotel_id,
                    Resena.procesada == True
                )
            )
        )
        
        if fecha_inicio:
            query = query.filter(Resena.fecha_publicacion >= fecha_inicio)
        if fecha_fin:
            query = query.filter(Resena.fecha_publicacion <= fecha_fin)
        
        # Última reseña
        ultima = query.order_by(Resena.fecha_publicacion.desc()).first()
        
        # Más positiva
        mas_positiva = query.order_by(Sentimiento.score_compuesto.desc()).first()
        
        # Más negativa
        mas_negativa = query.order_by(Sentimiento.score_compuesto.asc()).first()
        
        return {
            "ultima": ultima,
            "mas_positiva": mas_positiva,
            "mas_negativa": mas_negativa
        }
    
    def obtener_tendencia_temporal(
        self,
        db: Session,
        hotel_id: UUID,
        meses: int = 12
    ) -> List[Dict[str, any]]:
        """Obtener tendencia de indicadores por mes"""
        
        fecha_fin = datetime.utcnow()
        fecha_inicio = fecha_fin - timedelta(days=meses * 30)
        
        # Agrupar por mes
        resultados = (
            db.query(
                func.date_trunc('month', Resena.fecha_publicacion).label('mes'),
                func.count(Resena.id).label('total_resenas'),
                func.avg(Resena.puntuacion).label('promedio')
            )
            .join(HotelPlataforma)
            .filter(
                and_(
                    HotelPlataforma.hotel_id == hotel_id,
                    Resena.fecha_publicacion >= fecha_inicio,
                    Resena.fecha_publicacion <= fecha_fin,
                    Resena.procesada == True
                )
            )
            .group_by('mes')
            .order_by('mes')
            .all()
        )
        
        return [
            {
                "mes": mes.strftime("%Y-%m") if mes else "",
                "total_resenas": total,
                "promedio": round(float(promedio), 2) if promedio else 0.0
            }
            for mes, total, promedio in resultados
        ]


indicadores_service = IndicadoresService()
