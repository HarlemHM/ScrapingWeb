"""
Schemas de la aplicación
"""
from app.schemas.base import (
    BaseSchema,
    TimestampSchema,
    ResponseBase,
    ErrorResponse,
    PaginatedResponse,
)
from app.schemas.hotel import (
    HotelBase,
    HotelCreate,
    HotelUpdate,
    HotelRead,
    HotelWithStats,
)
from app.schemas.plataforma import (
    PlataformaBase,
    PlataformaCreate,
    PlataformaRead,
    HotelPlataformaBase,
    HotelPlataformaCreate,
    HotelPlataformaRead,
    HotelPlataformaWithInfo,
)
from app.schemas.resena import (
    ResenaBase,
    ResenaCreate,
    ResenaRead,
    SentimientoBase,
    SentimientoRead,
    ClasificacionBase,
    ClasificacionRead,
    ResenaWithAnalysis,
)
from app.schemas.scraping import (
    ScrapingRequest,
    ScrapingStatus,
    ScrapingResponse,
    ScrapingResult,
)
from app.schemas.criterio import (
    CriterioBase,
    CriterioCreate,
    CriterioRead,
)
from app.schemas.indicador import (
    IndicadorPeriodoBase,
    IndicadorPeriodoRead,
    IndicadoresResumen,
    ResenaDestacadaRead,
)
from app.schemas.export import (
    ExportRequest,
    ExportResponse,
    ExportStatus,
)

__all__ = [
    # Base
    "BaseSchema",
    "TimestampSchema",
    "ResponseBase",
    "ErrorResponse",
    "PaginatedResponse",
    # Hotel
    "HotelBase",
    "HotelCreate",
    "HotelUpdate",
    "HotelRead",
    "HotelWithStats",
    # Plataforma
    "PlataformaBase",
    "PlataformaCreate",
    "PlataformaRead",
    "HotelPlataformaBase",
    "HotelPlataformaCreate",
    "HotelPlataformaRead",
    "HotelPlataformaWithInfo",
    # Reseña
    "ResenaBase",
    "ResenaCreate",
    "ResenaRead",
    "SentimientoBase",
    "SentimientoRead",
    "ClasificacionBase",
    "ClasificacionRead",
    "ResenaWithAnalysis",
    # Scraping
    "ScrapingRequest",
    "ScrapingStatus",
    "ScrapingResponse",
    "ScrapingResult",
    # Criterio
    "CriterioBase",
    "CriterioCreate",
    "CriterioRead",
    # Indicador
    "IndicadorPeriodoBase",
    "IndicadorPeriodoRead",
    "IndicadoresResumen",
    "ResenaDestacadaRead",
    # Export
    "ExportRequest",
    "ExportResponse",
    "ExportStatus",
]
