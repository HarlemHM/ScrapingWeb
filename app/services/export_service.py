"""
Servicio de Exportación - Generación de reportes PDF y CSV
"""
import csv
from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import UUID
import io

from sqlalchemy.orm import Session
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT

from app.core.config import settings
from app.core.exceptions import ExportException
from app.crud import crud_hotel
from app.services.indicadores_service import indicadores_service


class ExportService:
    """Servicio de exportación de reportes"""
    
    def __init__(self):
        self.export_dir = Path(__file__).parent.parent.parent / "exports"
        self.export_dir.mkdir(exist_ok=True)
    
    def generar_csv(
        self,
        db: Session,
        hotel_id: UUID,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None
    ) -> str:
        """Generar reporte CSV"""
        
        hotel = crud_hotel.get(db, hotel_id)
        if not hotel:
            raise ExportException("Hotel no encontrado")
        
        # Obtener datos
        resumen = indicadores_service.obtener_resumen_hotel(
            db, hotel_id, fecha_inicio, fecha_fin
        )
        
        distribuciones = indicadores_service.obtener_distribucion_plataformas(
            db, fecha_inicio, fecha_fin
        )
        
        # Generar archivo
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_{hotel.nombre.replace(' ', '_')}_{timestamp}.csv"
        filepath = self.export_dir / filename
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Header
            writer.writerow(["Reporte de Análisis de Reseñas Hoteleras"])
            writer.writerow([f"Hotel: {hotel.nombre}"])
            writer.writerow([f"Fecha de generación: {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"])
            writer.writerow([])
            
            # Resumen general
            writer.writerow(["RESUMEN GENERAL"])
            writer.writerow(["Indicador", "Valor"])
            writer.writerow(["Total de Reseñas", resumen.total_resenas])
            writer.writerow(["Promedio Sostenibilidad", resumen.promedio_sostenibilidad])
            writer.writerow(["Promedio Calidad", resumen.promedio_calidad])
            writer.writerow(["Promedio General", resumen.promedio_general])
            writer.writerow(["% Reseñas Positivas", f"{resumen.porcentaje_positivas}%"])
            writer.writerow(["% Reseñas Negativas", f"{resumen.porcentaje_negativas}%"])
            writer.writerow(["% Reseñas Neutras", f"{resumen.porcentaje_neutras}%"])
            writer.writerow([])
            
            # Distribución por plataforma
            writer.writerow(["DISTRIBUCIÓN POR PLATAFORMA"])
            writer.writerow(["Plataforma", "Total Reseñas"])
            for dist in distribuciones:
                writer.writerow([dist["nombre"], dist["total"]])
        
        return str(filepath)
    
    def generar_pdf(
        self,
        db: Session,
        hotel_id: UUID,
        fecha_inicio: Optional[datetime] = None,
        fecha_fin: Optional[datetime] = None,
        incluir_graficos: bool = True
    ) -> str:
        """Generar reporte PDF"""
        
        hotel = crud_hotel.get(db, hotel_id)
        if not hotel:
            raise ExportException("Hotel no encontrado")
        
        # Obtener datos
        resumen = indicadores_service.obtener_resumen_hotel(
            db, hotel_id, fecha_inicio, fecha_fin
        )
        
        distribuciones = indicadores_service.obtener_distribucion_plataformas(
            db, fecha_inicio, fecha_fin
        )
        
        destacadas = indicadores_service.obtener_resenas_destacadas(
            db, hotel_id, fecha_inicio, fecha_fin
        )
        
        # Generar archivo
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"reporte_{hotel.nombre.replace(' ', '_')}_{timestamp}.pdf"
        filepath = self.export_dir / filename
        
        # Crear PDF
        doc = SimpleDocTemplate(str(filepath), pagesize=A4)
        story = []
        styles = getSampleStyleSheet()
        
        # Estilos personalizados
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1e3a8a'),
            alignment=TA_CENTER,
            spaceAfter=30
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2563eb'),
            spaceAfter=12
        )
        
        # Título
        story.append(Paragraph("Sistema de Análisis de Reseñas Hoteleras", title_style))
        story.append(Paragraph(f"<b>Hotel:</b> {hotel.nombre}", styles['Normal']))
        story.append(Paragraph(
            f"<b>Fecha de generación:</b> {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
            styles['Normal']
        ))
        story.append(Spacer(1, 0.3 * inch))
        
        # Resumen General
        story.append(Paragraph("Resumen General", heading_style))
        
        data_resumen = [
            ['Indicador', 'Valor'],
            ['Total de Reseñas', str(resumen.total_resenas)],
            ['Promedio Sostenibilidad', f"{resumen.promedio_sostenibilidad:.2f}/5.0"],
            ['Promedio Calidad', f"{resumen.promedio_calidad:.2f}/5.0"],
            ['Promedio General', f"{resumen.promedio_general:.2f}/5.0"],
            ['% Reseñas Positivas', f"{resumen.porcentaje_positivas:.1f}%"],
            ['% Reseñas Negativas', f"{resumen.porcentaje_negativas:.1f}%"],
            ['% Reseñas Neutras', f"{resumen.porcentaje_neutras:.1f}%"],
        ]
        
        table_resumen = Table(data_resumen, colWidths=[3.5 * inch, 2 * inch])
        table_resumen.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        story.append(table_resumen)
        story.append(Spacer(1, 0.3 * inch))
        
        # Distribución por Plataforma
        story.append(Paragraph("Distribución por Plataforma", heading_style))
        
        data_plat = [['Plataforma', 'Total Reseñas']]
        for dist in distribuciones:
            data_plat.append([dist["nombre"], str(dist["total"])])
        
        table_plat = Table(data_plat, colWidths=[3.5 * inch, 2 * inch])
        table_plat.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        story.append(table_plat)
        story.append(Spacer(1, 0.3 * inch))
        
        # Reseñas Destacadas
        if destacadas.get("mas_positiva"):
            story.append(PageBreak())
            story.append(Paragraph("Reseñas Destacadas", heading_style))
            
            # Más positiva
            mas_pos = destacadas["mas_positiva"]
            story.append(Paragraph("<b>Reseña Más Positiva:</b>", styles['Normal']))
            texto = mas_pos.texto_completo or f"{mas_pos.texto_positivo or ''} {mas_pos.texto_negativo or ''}"
            story.append(Paragraph(texto[:500], styles['Normal']))
            story.append(Spacer(1, 0.2 * inch))
            
            # Más negativa
            if destacadas.get("mas_negativa"):
                mas_neg = destacadas["mas_negativa"]
                story.append(Paragraph("<b>Reseña Más Negativa:</b>", styles['Normal']))
                texto_neg = mas_neg.texto_completo or f"{mas_neg.texto_positivo or ''} {mas_neg.texto_negativo or ''}"
                story.append(Paragraph(texto_neg[:500], styles['Normal']))
        
        # Construir PDF
        doc.build(story)
        
        return str(filepath)


export_service = ExportService()
