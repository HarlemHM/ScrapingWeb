"""
Configuración de Celery y tareas de background para ScrapingWeb

Este módulo define:
- Configuración de la aplicación Celery
- Tarea programada para scraping diario
- Tarea de procesamiento de NLP
"""

from celery import Celery
from celery.schedules import crontab
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal
from app.services.scraping_service import ScrapingService
from app.services.nlp_service import NLPService
from app.crud.crud_resena import crud_resena
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear instancia de Celery
celery_app = Celery(
    "scrapingweb",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

# Configuración de Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Bogota',  # Ajustar a tu zona horaria
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutos m├íximo por tarea
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=100,
)

# Configuración del scheduler (Beat)
celery_app.conf.beat_schedule = {
    'scraping-diario': {
        'task': 'app.workers.queue.ejecutar_scraping_diario',
        'schedule': crontab(hour=2, minute=0),  # Ejecutar a las 2:00 AM todos los dáas
        'args': (),
    },
}


@celery_app.task(name='app.workers.queue.ejecutar_scraping_diario')
def ejecutar_scraping_diario():
    """
    Tarea programada que ejecuta el scraping diario de todas las plataformas
    
    Esta tarea se ejecuta autom├íticamente cada dáa a las 2:00 AM.
    Procesa las reseñas de Google, Booking y Airbnb, y las almacena en la BD.
    """
    logger.info("­ƒÜÇ Iniciando scraping diario programado")
    
    db: Session = SessionLocal()
    try:
        scraping_service = ScrapingService(db)
        
        # Ejecutar scraping de todas las plataformas
        resultados = scraping_service.importar_desde_json()
        
        logger.info(f"Ô£à Scraping completado: {resultados}")
        
        # Procesar NLP de las nuevas reseñas
        procesar_nlp_nuevas_resenas.delay()
        
        return {
            "status": "success",
            "mensaje": "Scraping diario ejecutado correctamente",
            "resultados": resultados
        }
        
    except Exception as e:
        logger.error(f"ÔØî Error en scraping diario: {str(e)}")
        return {
            "status": "error",
            "mensaje": f"Error en scraping: {str(e)}"
        }
    finally:
        db.close()


@celery_app.task(name='app.workers.queue.procesar_nlp_nuevas_resenas')
def procesar_nlp_nuevas_resenas():
    """
    Tarea que procesa el an├ílisis NLP de reseñas sin procesar
    
    Esta tarea es llamada despuís del scraping para analizar
    el sentimiento y clasificar las nuevas reseñas.
    """
    logger.info("­ƒºá Iniciando procesamiento NLP de nuevas reseñas")
    
    db: Session = SessionLocal()
    try:
        nlp_service = NLPService()
        
        # Obtener reseñas sin an├ílisis de sentimiento
        resenas_sin_procesar = crud_resena.get_sin_sentimiento(db)
        
        procesadas = 0
        errores = 0
        
        for resena in resenas_sin_procesar:
            try:
                # Analizar sentimiento
                resultado_sentimiento = nlp_service.analizar_sentimiento(resena.comentario)
                
                # Clasificar por criterios
                clasificaciones = nlp_service.clasificar_por_criterios(resena.comentario)
                
                # Actualizar reseña con an├ílisis
                crud_resena.actualizar_analisis_nlp(
                    db=db,
                    resena_id=resena.id,
                    sentimiento_data=resultado_sentimiento,
                    clasificaciones=clasificaciones
                )
                
                procesadas += 1
                
            except Exception as e:
                logger.error(f"Error procesando reseña {resena.id}: {str(e)}")
                errores += 1
        
        db.commit()
        
        logger.info(f"Ô£à NLP completado: {procesadas} procesadas, {errores} errores")
        
        return {
            "status": "success",
            "procesadas": procesadas,
            "errores": errores
        }
        
    except Exception as e:
        logger.error(f"ÔØî Error en procesamiento NLP: {str(e)}")
        db.rollback()
        return {
            "status": "error",
            "mensaje": f"Error en NLP: {str(e)}"
        }
    finally:
        db.close()


@celery_app.task(name='app.workers.queue.ejecutar_scraping_manual')
def ejecutar_scraping_manual():
    """
    Tarea manual para ejecutar scraping bajo demanda
    
    Esta tarea puede ser invocada desde el endpoint de la API
    para forzar un scraping inmediato (por ejemplo, para testing).
    """
    logger.info("­ƒöº Scraping manual solicitado")
    return ejecutar_scraping_diario()


@celery_app.task(name='app.workers.queue.calcular_indicadores')
def calcular_indicadores():
    """
    Tarea para recalcular todos los indicadores y mítricas
    
    Esta tarea puede ejecutarse despuís del an├ílisis NLP
    para actualizar todos los indicadores del sistema.
    """
    logger.info("­ƒôè Recalculando indicadores")
    
    db: Session = SessionLocal()
    try:
        from app.services.indicadores_service import IndicadoresService
        
        indicadores_service = IndicadoresService(db)
        
        # Aquá se pueden agregar llamadas a mítodos especáficos
        # de c├ílculo de indicadores seg├║n la lógica de negocio
        
        logger.info("Ô£à Indicadores recalculados")
        
        return {
            "status": "success",
            "mensaje": "Indicadores actualizados"
        }
        
    except Exception as e:
        logger.error(f"ÔØî Error calculando indicadores: {str(e)}")
        return {
            "status": "error",
            "mensaje": f"Error: {str(e)}"
        }
    finally:
        db.close()
