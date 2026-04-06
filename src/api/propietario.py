from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud import propietario as crud_propietario

router = APIRouter(prefix="/propietarios", tags=["propietarios"])


class PropietarioCreate(BaseModel):
    id_propietario: UUID
    nombre: str
    telefono: str
    email: Optional[str] = None
    id_usuario_creacion: UUID


class PropietarioUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    id_usuario_edita: UUID


class PropietarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_propietario: UUID
    nombre: str
    telefono: str
    email: Optional[str] = None
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None
    id_usuario_creacion: UUID
    id_usuario_edita: Optional[UUID] = None


@router.get("", response_model=List[PropietarioRead])
def listar_propietarios(db: DbSession, skip: int = 0, limit: int = 100) -> List[PropietarioRead]:
    return crud_propietario.obtener_todos(db, skip=skip, limit=limit)


@router.get("/{id_propietario}", response_model=PropietarioRead)
def obtener_propietario(id_propietario: UUID) -> PropietarioRead:
    propietario = crud_propietario.obtener_por_id(id_propietario)
    if not propietario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Propietario no encontrado")
    return propietario


@router.post("", response_model=PropietarioRead, status_code=status.HTTP_201_CREATED)
def crear_propietario(body: PropietarioCreate) -> PropietarioRead:
    propietario = crud_propietario.crear(
        nombre=body.nombre,
        telefono=body.telefono,
        email=body.email,
        id_usuario_creacion=body.id_usuario_creacion,
    )
    return propietario


@router.put("/{id_propietario}", response_model=PropietarioRead)
def actualizar_propietario(id_propietario: UUID, body: PropietarioUpdate):
    id_edita = body.id_usuario_edita
    data = body.model_dump(exclude_unset=True, exclude={"id_usuario_edita"})
    propietario = crud_propietario.actualizar(id_propietario, id_usuario_edita=id_edita, **data)
    if not propietario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Propietario no encontrado")
    return propietario


@router.delete("/{id_propietario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_propietario(id_propietario: UUID) -> None:
    if not crud_propietario.eliminar(id_propietario):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Propietario no encontrado")