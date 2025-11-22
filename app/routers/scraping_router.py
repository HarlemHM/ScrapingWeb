"""
Router de Scraping - Simulación de scraping (real se ejecuta diariamente)
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.scraping import ScrapingResponse, ScrapingResult
from app.schemas.base import ResponseBase
from app.services.scraping_service import scraping_service

router = APIRouter()


@router.post("/ejecutar", response_model=ScrapingResponse)
def iniciar_scraping_simulado(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Endpoint para el frontend - NO ejecuta scraping real.
    El frontend muestra animación de carga, pero el scraping real
    se ejecuta automáticamente una vez al día mediante worker.
    """
    return ScrapingResponse(
        job_id="simulated-scraping-frontend",
        message="El scraping se ejecuta automáticamente cada día. Revisa los datos actualizados."
    )


@router.post("/ejecutar-ahora", response_model=ScrapingResult)
def ejecutar_scraping_manual(db: Session = Depends(get_db)):
    """
    Endpoint para ejecutar scraping manualmente (solo admin/testing).
    Este endpoint SÍ ejecuta el scraping real de los JSONs.
    """
    try:
        resultado = scraping_service.ejecutar_scraping_completo(db)
        
        total_nuevas = (
            resultado["google"]["nuevas"] +
            resultado["booking"]["nuevas"] +
            resultado["airbnb"]["nuevas"]
        )
        
        total_duplicadas = (
            resultado["google"]["duplicadas"] +
            resultado["booking"]["duplicadas"] +
            resultado["airbnb"]["duplicadas"]
        )
        
        return ScrapingResult(
            total_extraidas=total_nuevas + total_duplicadas,
            total_nuevas=total_nuevas,
            total_duplicadas=total_duplicadas,
            total_procesadas=resultado.get("procesadas_nlp", 0),
            errores=resultado.get("errores", []),
            tiempo_ejecucion=resultado.get("tiempo_ejecucion", 0.0)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error ejecutando scraping: {str(e)}"
        )


@router.get("/estado", response_model=ResponseBase)
def obtener_estado_scraping():
    """Obtener estado del sistema de scraping"""
    return ResponseBase(
        success=True,
        message="Sistema de scraping operativo. Ejecución automática programada diariamente."
    )
