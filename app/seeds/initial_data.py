"""
Datos iniciales - Seeds
"""
from sqlalchemy.orm import Session

from app.crud import crud_plataforma, crud_criterio
from app.schemas.plataforma import PlataformaCreate
from app.schemas.criterio import CriterioCreate


def init_plataformas(db: Session):
    """Crear plataformas iniciales"""
    plataformas = [
        {
            "codigo": "GOOGLE",
            "nombre": "Google Reviews",
            "descripcion": "Reseñas de Google Maps",
            "url_base": "https://www.google.com/maps",
            "icono": "google-icon.png"
        },
        {
            "codigo": "BOOKING",
            "nombre": "Booking.com",
            "descripcion": "Reseñas de Booking.com",
            "url_base": "https://www.booking.com",
            "icono": "booking-icon.png"
        },
        {
            "codigo": "AIRBNB",
            "nombre": "Airbnb",
            "descripcion": "Reseñas de Airbnb",
            "url_base": "https://www.airbnb.com",
            "icono": "airbnb-icon.png"
        },
        {
            "codigo": "TRIPADVISOR",
            "nombre": "TripAdvisor",
            "descripcion": "Reseñas de TripAdvisor",
            "url_base": "https://www.tripadvisor.com",
            "icono": "tripadvisor-icon.png"
        }
    ]
    
    for plat_data in plataformas:
        existing = crud_plataforma.get_by_codigo(db, codigo=plat_data["codigo"])
        if not existing:
            plat = PlataformaCreate(**plat_data)
            crud_plataforma.create(db, obj_in=plat)
            print(f"✅ Plataforma creada: {plat_data['nombre']}")


def init_criterios(db: Session):
    """Crear criterios de evaluación"""
    criterios = [
        {
            "codigo": "SOSTENIBILIDAD",
            "nombre": "Sostenibilidad",
            "descripcion": "Evaluación de prácticas sostenibles y ecológicas",
            "peso": 1.0,
            "palabras_clave": [
                "sostenible", "ecológico", "reciclaje", "energía solar",
                "medio ambiente", "verde", "orgánico", "reutilizable",
                "ahorro de agua", "ahorro de energía", "huerta", "productos locales",
                "biodegradable", "compostaje", "emisiones", "carbono neutral",
                "paneles solares", "eco-friendly", "sustentable"
            ]
        },
        {
            "codigo": "CALIDAD",
            "nombre": "Calidad",
            "descripcion": "Evaluación de calidad del servicio y instalaciones",
            "peso": 1.0,
            "palabras_clave": [
                "limpio", "limpieza", "cómodo", "confortable", "excelente",
                "servicio", "atención", "amable", "profesional", "puntual",
                "habitación", "instalaciones", "moderno", "nuevo", "mantenimiento",
                "desayuno", "comida", "restaurante", "piscina", "gym",
                "wifi", "internet", "aire acondicionado", "vista", "ubicación"
            ]
        }
    ]
    
    for crit_data in criterios:
        existing = crud_criterio.get_by_codigo(db, codigo=crit_data["codigo"])
        if not existing:
            crit = CriterioCreate(**crit_data)
            crud_criterio.create(db, obj_in=crit)
            print(f"✅ Criterio creado: {crit_data['nombre']}")


def init_db(db: Session):
    """Inicializar base de datos con datos semilla"""
    print("🌱 Iniciando seeds...")
    
    init_plataformas(db)
    init_criterios(db)
    
    print("✅ Seeds completados")


if __name__ == "__main__":
    from app.db.session import SessionLocal
    
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()
