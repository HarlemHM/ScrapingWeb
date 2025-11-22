"""
Router de Exportación - PDF y CSV
"""
from typing import Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.export import ExportRequest, ExportResponse
from app.services.export_service import export_service

router = APIRouter()


@router.post("/pdf", response_model=ExportResponse)
def exportar_pdf(
    hotel_id: UUID,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    incluir_graficos: bool = True,
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """
    Exportar reporte en PDF.
    El frontend muestra los botones "Exportar CSV" y "Exportar PDF".
    """
    try:
        filepath = export_service.generar_pdf(
            db, hotel_id, fecha_inicio, fecha_fin, incluir_graficos
        )
        
        return ExportResponse(
            job_id=f"pdf-{hotel_id}",
            message=f"PDF generado correctamente: {filepath}"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generando PDF: {str(e)}"
        )


@router.post("/csv", response_model=ExportResponse)
def exportar_csv(
    hotel_id: UUID,
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """
    Exportar reporte en CSV.
    """
    try:
        filepath = export_service.generar_csv(
            db, hotel_id, fecha_inicio, fecha_fin
        )
        
        return ExportResponse(
            job_id=f"csv-{hotel_id}",
            message=f"CSV generado correctamente: {filepath}"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generando CSV: {str(e)}"
        )


@router.get("/descargar/{filename}")
def descargar_archivo(filename: str):
    """Descargar archivo exportado"""
    from pathlib import Path
    
    export_dir = Path(__file__).parent.parent.parent / "exports"
    filepath = export_dir / filename
    
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    return FileResponse(
        path=str(filepath),
        filename=filename,
        media_type='application/octet-stream'
    )
