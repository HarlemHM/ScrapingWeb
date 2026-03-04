"""
CRUD operations
"""
from app.crud.base import CRUDBase
from app.crud.crud_hotel import crud_hotel
from app.crud.crud_plataforma import crud_plataforma, crud_hotel_plataforma
from app.crud.crud_resena import crud_resena, crud_sentimiento, crud_clasificacion
from app.crud.crud_criterio import crud_criterio
from app.crud.crud_indicador import crud_indicador_periodo, crud_resena_destacada

__all__ = [
    "CRUDBase",
    "crud_hotel",
    "crud_plataforma",
    "crud_hotel_plataforma",
    "crud_resena",
    "crud_sentimiento",
    "crud_clasificacion",
    "crud_criterio",
    "crud_indicador_periodo",
    "crud_resena_destacada",
]
