"""
Router de Hoteles
"""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.crud import crud_hotel
from app.schemas.hotel import HotelCreate, HotelUpdate, HotelRead, HotelWithStats
from app.schemas.base import ResponseBase

router = APIRouter()


@router.get("/", response_model=List[HotelRead])
def listar_hoteles(
    skip: int = 0,
    limit: int = 100,
    activos_solo: bool = True,
    db: Session = Depends(get_db)
):
    """Listar todos los hoteles"""
    if activos_solo:
        hoteles = crud_hotel.get_active(db, skip=skip, limit=limit)
    else:
        hoteles = crud_hotel.get_multi(db, skip=skip, limit=limit)
    return hoteles


@router.get("/{hotel_id}", response_model=HotelRead)
def obtener_hotel(hotel_id: UUID, db: Session = Depends(get_db)):
    """Obtener un hotel por ID"""
    hotel = crud_hotel.get(db, hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel no encontrado")
    return hotel


@router.get("/{hotel_id}/stats", response_model=HotelWithStats)
def obtener_hotel_con_estadisticas(hotel_id: UUID, db: Session = Depends(get_db)):
    """Obtener hotel con estadísticas"""
    result = crud_hotel.get_with_stats(db, hotel_id=hotel_id)
    if not result:
        raise HTTPException(status_code=404, detail="Hotel no encontrado")
    
    hotel_data = result["hotel"].__dict__.copy()
    hotel_data["total_resenas"] = result["total_resenas"]
    hotel_data["promedio_calificacion"] = result["promedio_calificacion"]
    hotel_data["ultimo_scraping"] = result["ultimo_scraping"]
    
    return hotel_data


@router.post("/", response_model=HotelRead, status_code=status.HTTP_201_CREATED)
def crear_hotel(hotel_in: HotelCreate, db: Session = Depends(get_db)):
    """Crear un nuevo hotel"""
    # Verificar si ya existe
    existing = crud_hotel.get_by_nombre(db, nombre=hotel_in.nombre)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un hotel con ese nombre"
        )
    
    hotel = crud_hotel.create(db, obj_in=hotel_in)
    return hotel


@router.put("/{hotel_id}", response_model=HotelRead)
def actualizar_hotel(
    hotel_id: UUID,
    hotel_in: HotelUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un hotel"""
    hotel = crud_hotel.get(db, hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel no encontrado")
    
    hotel = crud_hotel.update(db, db_obj=hotel, obj_in=hotel_in)
    return hotel


@router.delete("/{hotel_id}", response_model=ResponseBase)
def eliminar_hotel(hotel_id: UUID, db: Session = Depends(get_db)):
    """Eliminar un hotel (soft delete)"""
    hotel = crud_hotel.get(db, hotel_id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel no encontrado")
    
    # Soft delete
    crud_hotel.update(db, db_obj=hotel, obj_in={"activo": False})
    
    return ResponseBase(message="Hotel eliminado correctamente")
