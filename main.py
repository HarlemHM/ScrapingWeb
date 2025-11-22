"""
Aplicación principal FastAPI
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.events import lifespan
from app.core.exceptions import (
    ScrapingException,
    NLPException,
    ExportException,
    NotFoundException,
    AlreadyExistsException,
    ValidationException
)
from fastapi import Request, status
from fastapi.responses import JSONResponse

# Importar routers
from app.routers import (
    hotels_router,
    scraping_router,
    resenas_router,
    indicadores_router,
    export_router
)


# Crear aplicación
app = FastAPI(
    title="ScrapingWeb - Sistema de Análisis de Reseñas Hoteleras",
    description="Backend para análisis de sostenibilidad y calidad de hoteles mediante scraping de reseñas",
    version="1.0.0",
    lifespan=lifespan
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception Handlers
@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"success": False, "message": str(exc), "detail": exc.detail}
    )


@app.exception_handler(AlreadyExistsException)
async def already_exists_exception_handler(request: Request, exc: AlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"success": False, "message": str(exc), "detail": exc.detail}
    )


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"success": False, "message": str(exc), "detail": exc.detail}
    )


@app.exception_handler(ScrapingException)
async def scraping_exception_handler(request: Request, exc: ScrapingException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"success": False, "message": str(exc), "detail": exc.detail}
    )


@app.exception_handler(NLPException)
async def nlp_exception_handler(request: Request, exc: NLPException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"success": False, "message": str(exc), "detail": exc.detail}
    )


@app.exception_handler(ExportException)
async def export_exception_handler(request: Request, exc: ExportException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"success": False, "message": str(exc), "detail": exc.detail}
    )


# Rutas principales
@app.get("/")
async def root():
    return {
        "app": "ScrapingWeb - Sistema de Análisis de Reseñas Hoteleras",
        "version": "1.0.0",
        "description": "API para análisis de sostenibilidad y calidad hotelera"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}


# Registrar routers
app.include_router(
    hotels_router.router,
    prefix="/api/v1/hoteles",
    tags=["Hoteles"]
)

app.include_router(
    scraping_router.router,
    prefix="/api/v1/scraping",
    tags=["Scraping"]
)

app.include_router(
    resenas_router.router,
    prefix="/api/v1/resenas",
    tags=["Reseñas"]
)

app.include_router(
    indicadores_router.router,
    prefix="/api/v1/indicadores",
    tags=["Indicadores"]
)

app.include_router(
    export_router.router,
    prefix="/api/v1/export",
    tags=["Exportación"]
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
