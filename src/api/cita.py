from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from src.crud import cita as crud_cita

router = APIRouter(prefix="/citas", tags=["citas"])


class CitaCreate(BaseModel):
    id_mascota: UUID
    id_usuario_agenda: UUID
    motivo: str
    costo: float
    lugar: Optional[str] = None


class CitaUpdate(BaseModel):
    motivo: Optional[str] = None
    costo: Optional[float] = None
    lugar: Optional[str] = None
    estado: Optional[str] = None


class CitaRead(BaseModel):
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
def listar_citas(skip: int = 0, limit: int = 100) -> List[CitaRead]:
    return crud_cita.listar(skip=skip, limit=limit)


@router.get("/{id_cita}", response_model=CitaRead)
def obtener_cita(id_cita: UUID) -> CitaRead:
    c = crud_cita.obtener(id_cita)
    if not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
        )
    return c


@router.post("", response_model=CitaRead, status_code=status.HTTP_201_CREATED)
def crear_cita(body: CitaCreate) -> CitaRead:
    return crud_cita.crear(
        id_mascota=body.id_mascota,
        id_usuario_agenda=body.id_usuario_agenda,
        motivo=body.motivo,
        costo=body.costo,
        lugar=body.lugar,
    )


@router.put("/{id_cita}", response_model=CitaRead)
def actualizar_cita(id_cita: UUID, body: CitaUpdate) -> CitaRead:
    data = body.model_dump(exclude_unset=True)
    c = crud_cita.actualizar(id_cita, **data)
    if not c:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
        )
    return c


@router.delete("/{id_cita}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cita(id_cita: UUID) -> None:
    if not crud_cita.eliminar(id_cita):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada"
        )
