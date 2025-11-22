"""
CRUD para Criterio
"""
from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.criterio import Criterio
from app.schemas.criterio import CriterioCreate


class CRUDCriterio(CRUDBase[Criterio, CriterioCreate, dict]):
    """CRUD para Criterio"""
    
    def get_by_codigo(self, db: Session, *, codigo: str) -> Optional[Criterio]:
        """Obtener criterio por código"""
        return db.query(Criterio).filter(Criterio.codigo == codigo).first()
    
    def get_active(self, db: Session) -> List[Criterio]:
        """Obtener criterios activos"""
        return db.query(Criterio).filter(Criterio.activo == True).all()


crud_criterio = CRUDCriterio(Criterio)
