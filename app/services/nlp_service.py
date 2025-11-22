"""
Servicio de NLP - Procesamiento de lenguaje natural
"""
import re
from typing import Dict, List, Optional
from datetime import datetime

from sqlalchemy.orm import Session
from textblob import TextBlob
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

from app.core.config import settings
from app.core.exceptions import NLPException
from app.crud import crud_resena, crud_sentimiento, crud_clasificacion, crud_criterio
from app.models.resena import Resena
from app.schemas.resena import SentimientoBase, ClasificacionBase


# Descargar recursos NLTK si no existen
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)


class NLPService:
    """Servicio de procesamiento de lenguaje natural"""
    
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        # Palabras clave para sostenibilidad
        self.sostenibilidad_keywords = [
            'sostenible', 'ecológico', 'reciclaje', 'energía solar',
            'medio ambiente', 'verde', 'orgánico', 'reutilizable',
            'ahorro de agua', 'ahorro de energía', 'huerta', 'productos locales',
            'biodegradable', 'compostaje', 'emisiones', 'carbono neutral'
        ]
        # Palabras clave para calidad
        self.calidad_keywords = [
            'limpio', 'limpieza', 'cómodo', 'confortable', 'excelente',
            'servicio', 'atención', 'amable', 'profesional', 'puntual',
            'habitación', 'instalaciones', 'moderno', 'nuevo', 'mantenimiento',
            'desayuno', 'comida', 'restaurante', 'piscina', 'gym'
        ]
    
    def limpiar_texto(self, texto: str) -> str:
        """Limpiar y normalizar texto"""
        if not texto:
            return ""
        # Convertir a minúsculas
        texto = texto.lower()
        # Eliminar URLs
        texto = re.sub(r'http\S+|www.\S+', '', texto)
        # Eliminar caracteres especiales pero mantener espacios y puntuación básica
        texto = re.sub(r'[^\w\s.,;:!?áéíóúñü]', '', texto)
        # Eliminar espacios múltiples
        texto = re.sub(r'\s+', ' ', texto)
        return texto.strip()
    
    def analizar_sentimiento(self, texto: str) -> Dict[str, float]:
        """Analizar sentimiento usando VADER"""
        texto_limpio = self.limpiar_texto(texto)
        
        if not texto_limpio:
            return {
                'positivo': 0.0,
                'negativo': 0.0,
                'neutro': 1.0,
                'compuesto': 0.0
            }
        
        # VADER scores
        scores = self.sia.polarity_scores(texto_limpio)
        
        return {
            'positivo': scores['pos'],
            'negativo': scores['neg'],
            'neutro': scores['neu'],
            'compuesto': scores['compound']
        }
    
    def clasificar_sentimiento(self, score_compuesto: float) -> str:
        """Clasificar sentimiento basado en score compuesto"""
        if score_compuesto >= settings.NLP_POSITIVE_THRESHOLD:
            return "POSITIVO"
        elif score_compuesto <= settings.NLP_NEGATIVE_THRESHOLD:
            return "NEGATIVO"
        else:
            return "NEUTRO"
    
    def calcular_confianza(self, scores: Dict[str, float]) -> float:
        """Calcular confianza del análisis"""
        # La confianza es alta cuando hay polaridad clara
        max_score = max(scores['positivo'], scores['negativo'])
        return min(max_score * 1.5, 1.0)
    
    def clasificar_por_criterio(
        self, texto: str, criterio_keywords: List[str]
    ) -> Dict[str, any]:
        """Clasificar texto según palabras clave de un criterio"""
        texto_limpio = self.limpiar_texto(texto)
        palabras_detectadas = []
        
        # Buscar palabras clave
        for keyword in criterio_keywords:
            if keyword.lower() in texto_limpio:
                palabras_detectadas.append(keyword)
        
        # Si no hay palabras clave, valoración neutral
        if not palabras_detectadas:
            return {
                'valoracion': 3.0,
                'confianza': 0.0,
                'palabras_detectadas': []
            }
        
        # Analizar sentimiento del texto
        sentimiento = self.analizar_sentimiento(texto)
        
        # Valoración basada en sentimiento (1-5)
        # compuesto va de -1 a 1, convertir a escala 1-5
        valoracion = ((sentimiento['compuesto'] + 1) / 2) * 4 + 1
        valoracion = max(1.0, min(5.0, valoracion))
        
        # Confianza basada en cantidad de palabras clave y polaridad
        confianza = min(len(palabras_detectadas) * 0.2, 1.0)
        
        return {
            'valoracion': round(valoracion, 2),
            'confianza': round(confianza, 2),
            'palabras_detectadas': palabras_detectadas
        }
    
    def procesar_resena(self, db: Session, resena: Resena) -> bool:
        """Procesar una reseña completa: sentimiento y clasificaciones"""
        try:
            # Obtener texto completo
            texto = resena.texto_completo or ""
            if not texto and (resena.texto_positivo or resena.texto_negativo):
                texto = f"{resena.texto_positivo or ''} {resena.texto_negativo or ''}"
            
            if not texto.strip():
                return False
            
            # 1. Análisis de sentimiento
            scores = self.analizar_sentimiento(texto)
            tipo_sentimiento = self.clasificar_sentimiento(scores['compuesto'])
            confianza = self.calcular_confianza(scores)
            
            # Crear sentimiento
            sentimiento_data = SentimientoBase(
                tipo_sentimiento=tipo_sentimiento,
                score_positivo=scores['positivo'],
                score_negativo=scores['negativo'],
                score_neutro=scores['neutro'],
                score_compuesto=scores['compuesto'],
                confianza=confianza
            )
            
            # Guardar sentimiento
            sentimiento_dict = sentimiento_data.model_dump()
            sentimiento_dict['resena_id'] = resena.id
            crud_sentimiento.create(db, obj_in=sentimiento_dict)
            
            # 2. Clasificación por criterios
            criterios = crud_criterio.get_active(db)
            
            for criterio in criterios:
                if criterio.codigo == "SOSTENIBILIDAD":
                    keywords = criterio.palabras_clave or self.sostenibilidad_keywords
                elif criterio.codigo == "CALIDAD":
                    keywords = criterio.palabras_clave or self.calidad_keywords
                else:
                    keywords = criterio.palabras_clave or []
                
                resultado = self.clasificar_por_criterio(texto, keywords)
                
                # Crear clasificación
                clasificacion_data = ClasificacionBase(
                    criterio_id=criterio.id,
                    valoracion=resultado['valoracion'],
                    confianza=resultado['confianza'],
                    palabras_detectadas=resultado['palabras_detectadas']
                )
                
                # Guardar clasificación
                clasificacion_dict = clasificacion_data.model_dump()
                clasificacion_dict['resena_id'] = resena.id
                crud_clasificacion.create(db, obj_in=clasificacion_dict)
            
            # 3. Marcar reseña como procesada
            crud_resena.mark_as_processed(db, resena_id=resena.id)
            
            return True
            
        except Exception as e:
            raise NLPException(f"Error procesando reseña {resena.id}: {str(e)}")
    
    def procesar_pendientes(self, db: Session, limit: int = 100) -> int:
        """Procesar todas las reseñas pendientes"""
        resenas = crud_resena.get_pending_processing(db, limit=limit)
        procesadas = 0
        
        for resena in resenas:
            try:
                if self.procesar_resena(db, resena):
                    procesadas += 1
            except Exception:
                continue
        
        return procesadas


nlp_service = NLPService()
