"""
CRUD para IndicadorPeriodo y ResenaDestacada
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.crud.base import CRUDBase
from app.models.indicador_periodo import IndicadorPeriodo
from app.models.resena_destacada import ResenaDestacada
from app.schemas.indicador import IndicadorPeriodoBase


class CRUDIndicadorPeriodo(CRUDBase[IndicadorPeriodo, IndicadorPeriodoBase, dict]):
    """CRUD para IndicadorPeriodo"""
    
    def get_by_hotel_and_periodo(
        self,
        db: Session,
        *,
        hotel_id: UUID,
        periodo_inicio: datetime,
        periodo_fin: datetime
    ) -> Optional[IndicadorPeriodo]:
        """Obtener indicador de un hotel en un período"""
        return (
            db.query(IndicadorPeriodo)
            .filter(
                and_(
                    IndicadorPeriodo.hotel_id == hotel_id,
                    IndicadorPeriodo.periodo_inicio == periodo_inicio,
                    IndicadorPeriodo.periodo_fin == periodo_fin
                )
            )
            .first()
        )
    
    def get_by_hotel(
        self, db: Session, *, hotel_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[IndicadorPeriodo]:
        """Obtener indicadores de un hotel"""
        return (
            db.query(IndicadorPeriodo)
            .filter(IndicadorPeriodo.hotel_id == hotel_id)
            .order_by(IndicadorPeriodo.periodo_inicio.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


class CRUDResenaDestacada(CRUDBase[ResenaDestacada, dict, dict]):
    """CRUD para ResenaDestacada"""
    
    def get_by_hotel_and_tipo(
        self, db: Session, *, hotel_id: UUID, tipo: str
    ) -> Optional[ResenaDestacada]:
        """Obtener reseña destacada de un hotel por tipo"""
        return (
            db.query(ResenaDestacada)
            .filter(
                ResenaDestacada.hotel_id == hotel_id,
                ResenaDestacada.tipo == tipo
            )
            .first()
        )


crud_indicador_periodo = CRUDIndicadorPeriodo(IndicadorPeriodo)
crud_resena_destacada = CRUDResenaDestacada(ResenaDestacada)
