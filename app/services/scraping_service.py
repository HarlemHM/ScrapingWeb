"""
Servicio de Scraping - Importación y procesamiento de reseñas
"""
import json
from typing import Dict, List
from datetime import datetime
from pathlib import Path
from dateutil import parser

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import ScrapingException
from app.crud import crud_hotel, crud_plataforma, crud_hotel_plataforma, crud_resena
from app.schemas.resena import ResenaCreate
from app.services.nlp_service import nlp_service


class ScrapingService:
    """Servicio de scraping e importación de reseñas"""
    
    def __init__(self):
        self.scraping_dir = Path(__file__).parent.parent / "scraping"
    
    def parsear_fecha_google(self, fecha_str: str) -> datetime:
        """Parsear fecha de Google Reviews"""
        if not fecha_str or fecha_str == "Fecha estimada no disponible":
            return datetime.utcnow()
        try:
            return parser.parse(fecha_str)
        except:
            return datetime.utcnow()
    
    def parsear_fecha_booking(self, registro: str) -> datetime:
        """Parsear fecha de Booking"""
        # "Fecha del comentario: 18 de septiembre de 2025"
        if not registro:
            return datetime.utcnow()
        try:
            fecha_parte = registro.split(": ")[-1]
            return parser.parse(fecha_parte, dayfirst=True)
        except:
            return datetime.utcnow()
    
    def parsear_fecha_airbnb(self, fecha_str: str) -> datetime:
        """Parsear fecha de Airbnb"""
        # "agosto de 2025" o "Hace 2 semanas"
        if not fecha_str:
            return datetime.utcnow()
        
        if "Hace" in fecha_str:
            return datetime.utcnow()  # Aproximación
        
        try:
            # Mapeo de meses en español
            meses = {
                'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
                'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
                'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
            }
            
            for mes_nombre, mes_num in meses.items():
                if mes_nombre in fecha_str.lower():
                    año = fecha_str.split()[-1]
                    return datetime(int(año), mes_num, 1)
            
            return datetime.utcnow()
        except:
            return datetime.utcnow()
    
    def normalizar_puntuacion(self, puntuacion: any, plataforma: str) -> float:
        """Normalizar puntuación a escala 1-5"""
        if plataforma == "GOOGLE":
            # "4/5" -> 4.0
            if isinstance(puntuacion, str) and "/" in puntuacion:
                return float(puntuacion.split("/")[0])
            return float(puntuacion)
        
        elif plataforma == "BOOKING":
            # "8,0" -> 4.0 (escala 10 a 5)
            if isinstance(puntuacion, str):
                puntuacion = puntuacion.replace(",", ".")
            return float(puntuacion) / 2
        
        elif plataforma == "AIRBNB":
            # Ya está en escala 1-5
            return float(puntuacion)
        
        return 3.0
    
    def importar_desde_google(self, db: Session, hotel_id: str) -> Dict[str, int]:
        """Importar reseñas desde JSON de Google"""
        archivo = self.scraping_dir / "reseñas_google.json"
        
        if not archivo.exists():
            raise ScrapingException(f"Archivo no encontrado: {archivo}")
        
        with open(archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Obtener plataforma Google
        plataforma = crud_plataforma.get_by_codigo(db, codigo="GOOGLE")
        if not plataforma:
            raise ScrapingException("Plataforma GOOGLE no encontrada en base de datos")
        
        total_nuevas = 0
        total_duplicadas = 0
        
        # Iterar por ciudades
        for ciudad, hoteles in data.items():
            for hotel_data in hoteles:
                nombre_hotel = hotel_data.get("nombre", "")
                
                # Buscar hotel por nombre
                hotel = crud_hotel.get_by_nombre(db, nombre=nombre_hotel)
                if not hotel:
                    continue
                
                # Obtener o crear relación hotel-plataforma
                hp = crud_hotel_plataforma.get_by_hotel_and_plataforma(
                    db, hotel_id=hotel.id, plataforma_id=plataforma.id
                )
                if not hp:
                    from app.schemas.plataforma import HotelPlataformaCreate
                    hp_data = HotelPlataformaCreate(
                        hotel_id=hotel.id,
                        plataforma_id=plataforma.id,
                        url_hotel=hotel_data.get("url", "")
                    )
                    hp = crud_hotel_plataforma.create(db, obj_in=hp_data)
                
                # Procesar comentarios
                for comentario in hotel_data.get("comentarios", []):
                    try:
                        resena_data = ResenaCreate(
                            hotel_plataforma_id=hp.id,
                            nombre_autor=comentario.get("usuario", "Anónimo"),
                            texto_completo=comentario.get("texto", ""),
                            puntuacion=self.normalizar_puntuacion(
                                comentario.get("puntuacion", "3/5"), "GOOGLE"
                            ),
                            fecha_publicacion=self.parsear_fecha_google(
                                comentario.get("fecha", "")
                            )
                        )
                        
                        # Crear con hash para evitar duplicados
                        resena = crud_resena.create_with_hash(db, obj_in=resena_data)
                        
                        if resena.procesada:
                            total_duplicadas += 1
                        else:
                            total_nuevas += 1
                            
                    except Exception:
                        continue
        
        return {"nuevas": total_nuevas, "duplicadas": total_duplicadas}
    
    def importar_desde_booking(self, db: Session) -> Dict[str, int]:
        """Importar reseñas desde JSON de Booking"""
        archivo = self.scraping_dir / "reseñas_booking.json"
        
        if not archivo.exists():
            raise ScrapingException(f"Archivo no encontrado: {archivo}")
        
        with open(archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        plataforma = crud_plataforma.get_by_codigo(db, codigo="BOOKING")
        if not plataforma:
            raise ScrapingException("Plataforma BOOKING no encontrada")
        
        total_nuevas = 0
        total_duplicadas = 0
        
        for comentario_data in data.get("comentarios_parciales", []):
            nombre_hotel = comentario_data.get("hotel", "")
            hotel = crud_hotel.get_by_nombre(db, nombre=nombre_hotel)
            
            if not hotel:
                continue
            
            hp = crud_hotel_plataforma.get_by_hotel_and_plataforma(
                db, hotel_id=hotel.id, plataforma_id=plataforma.id
            )
            if not hp:
                from app.schemas.plataforma import HotelPlataformaCreate
                hp_data = HotelPlataformaCreate(
                    hotel_id=hotel.id,
                    plataforma_id=plataforma.id,
                    url_hotel=comentario_data.get("url", "")
                )
                hp = crud_hotel_plataforma.create(db, obj_in=hp_data)
            
            try:
                resena_data = ResenaCreate(
                    hotel_plataforma_id=hp.id,
                    nombre_autor=comentario_data.get("usuario", "Anónimo"),
                    texto_positivo=comentario_data.get("positivo", ""),
                    texto_negativo=comentario_data.get("negativo", ""),
                    puntuacion=self.normalizar_puntuacion(
                        comentario_data.get("puntuacion", "5,0"), "BOOKING"
                    ),
                    fecha_publicacion=self.parsear_fecha_booking(
                        comentario_data.get("Registro", "")
                    )
                )
                
                resena = crud_resena.create_with_hash(db, obj_in=resena_data)
                
                if resena.procesada:
                    total_duplicadas += 1
                else:
                    total_nuevas += 1
                    
            except Exception:
                continue
        
        return {"nuevas": total_nuevas, "duplicadas": total_duplicadas}
    
    def importar_desde_airbnb(self, db: Session) -> Dict[str, int]:
        """Importar reseñas desde JSON de Airbnb"""
        archivo = self.scraping_dir / "reseñas_airbnb.json"
        
        if not archivo.exists():
            raise ScrapingException(f"Archivo no encontrado: {archivo}")
        
        with open(archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        plataforma = crud_plataforma.get_by_codigo(db, codigo="AIRBNB")
        if not plataforma:
            raise ScrapingException("Plataforma AIRBNB no encontrada")
        
        total_nuevas = 0
        total_duplicadas = 0
        
        # Agrupar por alojamiento
        alojamientos = {}
        for resena_data in data:
            room_id = resena_data.get("room_id", "")
            titulo = resena_data.get("titulo_alojamiento", "")
            
            if room_id not in alojamientos:
                alojamientos[room_id] = {
                    "titulo": titulo,
                    "url": resena_data.get("url_alojamiento", ""),
                    "resenas": []
                }
            alojamientos[room_id]["resenas"].append(resena_data)
        
        # Procesar cada alojamiento
        for room_id, aloj_data in alojamientos.items():
            # Buscar hotel por nombre similar
            titulo = aloj_data["titulo"]
            hotel = crud_hotel.get_by_nombre(db, nombre=titulo)
            
            if not hotel:
                # Intentar buscar por nombre parcial
                continue
            
            hp = crud_hotel_plataforma.get_by_hotel_and_plataforma(
                db, hotel_id=hotel.id, plataforma_id=plataforma.id
            )
            if not hp:
                from app.schemas.plataforma import HotelPlataformaCreate
                hp_data = HotelPlataformaCreate(
                    hotel_id=hotel.id,
                    plataforma_id=plataforma.id,
                    url_hotel=aloj_data["url"],
                    identificador_externo=room_id
                )
                hp = crud_hotel_plataforma.create(db, obj_in=hp_data)
            
            for resena_raw in aloj_data["resenas"]:
                try:
                    comentario = resena_raw.get("comentario", "")
                    if comentario == "N/A":
                        comentario = ""
                    
                    resena_data = ResenaCreate(
                        hotel_plataforma_id=hp.id,
                        nombre_autor=resena_raw.get("nombre", "Anónimo"),
                        ubicacion_autor=resena_raw.get("ubicacion", ""),
                        texto_completo=comentario,
                        puntuacion=float(resena_raw.get("puntuacion", 5)),
                        fecha_publicacion=self.parsear_fecha_airbnb(
                            resena_raw.get("fecha", "")
                        ),
                        tipo_estadia=resena_raw.get("tipo_estadia", "")
                    )
                    
                    resena = crud_resena.create_with_hash(db, obj_in=resena_data)
                    
                    if resena.procesada:
                        total_duplicadas += 1
                    else:
                        total_nuevas += 1
                        
                except Exception:
                    continue
        
        return {"nuevas": total_nuevas, "duplicadas": total_duplicadas}
    
    def ejecutar_scraping_completo(self, db: Session) -> Dict[str, any]:
        """Ejecutar scraping completo de todas las plataformas"""
        inicio = datetime.utcnow()
        resultados = {
            "google": {"nuevas": 0, "duplicadas": 0},
            "booking": {"nuevas": 0, "duplicadas": 0},
            "airbnb": {"nuevas": 0, "duplicadas": 0},
            "errores": []
        }
        
        # Google
        try:
            resultados["google"] = self.importar_desde_google(db, hotel_id=None)
        except Exception as e:
            resultados["errores"].append(f"Google: {str(e)}")
        
        # Booking
        try:
            resultados["booking"] = self.importar_desde_booking(db)
        except Exception as e:
            resultados["errores"].append(f"Booking: {str(e)}")
        
        # Airbnb
        try:
            resultados["airbnb"] = self.importar_desde_airbnb(db)
        except Exception as e:
            resultados["errores"].append(f"Airbnb: {str(e)}")
        
        # Procesar NLP
        try:
            procesadas = nlp_service.procesar_pendientes(db, limit=500)
            resultados["procesadas_nlp"] = procesadas
        except Exception as e:
            resultados["errores"].append(f"NLP: {str(e)}")
        
        fin = datetime.utcnow()
        resultados["tiempo_ejecucion"] = (fin - inicio).total_seconds()
        
        return resultados


scraping_service = ScrapingService()
