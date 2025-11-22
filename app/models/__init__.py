"""
Modelos de la aplicación
"""
from app.models.hotel import Hotel
from app.models.plataforma import Plataforma
from app.models.hotel_plataforma import HotelPlataforma
from app.models.resena import Resena
from app.models.sentimiento import Sentimiento
from app.models.criterio import Criterio
from app.models.clasificacion import Clasificacion
from app.models.indicador_periodo import IndicadorPeriodo
from app.models.resena_destacada import ResenaDestacada

__all__ = [
    "Hotel",
    "Plataforma",
    "HotelPlataforma",
    "Resena",
    "Sentimiento",
    "Criterio",
    "Clasificacion",
    "IndicadorPeriodo",
    "ResenaDestacada",
]
