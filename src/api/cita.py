"""
Endpoints para la entidad Cita.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.crud import cita as crud_cita

router = APIRouter(prefix="/citas", tags=["citas"])


class CitaCreate(BaseModel):
    """
    Esquema para crear una nueva cita.
    """

    id_mascota: UUID
    id_usuario_agenda: UUID
    motivo: str
    costo: float
    lugar: Optional[str] = None


class CitaUpdate(BaseModel):
    """
    Esquema para actualizar una cita existente.
    """

    motivo: Optional[str] = None
    costo: Optional[float] = None
    lugar: Optional[str] = None
    estado: Optional[str] = None


class CitaRead(BaseModel):
    """
    Esquema de respuesta para una cita.
    """

    model_config = ConfigDict(from_attributes=True)

    id_cita: UUID
    id_mascota: UUID
    id_usuario_agenda: UUID
    motivo: str
    costo: float
    lugar: Optional[str] = None
    estado: str
    fecha_hora: datetime


@router.get("", response_model=List[CitaRead])
def listar_citas(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[CitaRead]:
    """
    Lista todas las citas con paginacion.
    """
    return crud_cita.listar(db, skip=skip, limit=limit)


@router.get("/{id_cita}", response_model=CitaRead)
def obtener_cita(id_cita: UUID, db: Session = Depends(get_db)) -> CitaRead:
    """
    Obtiene una cita por su ID.
    """
    c = crud_cita.obtener(db, id_cita)
    if not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
        )
    return c


@router.post("", response_model=CitaRead, status_code=status.HTTP_201_CREATED)
def crear_cita(body: CitaCreate, db: Session = Depends(get_db)) -> CitaRead:
    """
    Crea una nueva cita en el sistema.
    """
    try:
        return crud_cita.crear(
            db=db,
            id_mascota=body.id_mascota,
            id_usuario_agenda=body.id_usuario_agenda,
            motivo=body.motivo,
            costo=body.costo,
            lugar=body.lugar,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id_cita}", response_model=CitaRead)
def actualizar_cita(
    id_cita: UUID, body: CitaUpdate, db: Session = Depends(get_db)
) -> CitaRead:
    """
    Actualiza una cita existente.
    """
    data = body.model_dump(exclude_unset=True)
    c = crud_cita.actualizar(db, id_cita, **data)
    if not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
        )
    return c


@router.delete("/{id_cita}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cita(id_cita: UUID, db: Session = Depends(get_db)) -> None:
    """
    Elimina una cita por su ID.
    """
    if not crud_cita.eliminar(db, id_cita):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
        )
