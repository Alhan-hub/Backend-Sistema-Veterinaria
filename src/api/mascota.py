from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from src.crud import mascota as crud_mascota

router = APIRouter(prefix="/mascotas", tags=["mascotas"])


class MascotaCreate(BaseModel):
    nombre: str
    id_propietario: UUID
    id_usuario_creacion: UUID
    edad: int
    tipo_mascota: str
    raza: Optional[str] = None


class MascotaUpdate(BaseModel):
    nombre: Optional[str] = None
    id_propietario: Optional[UUID] = None
    edad: Optional[int] = None
    tipo_mascota: Optional[str] = None
    raza: Optional[str] = None
    id_usuario_edita: Optional[UUID] = None


class MascotaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_mascota: UUID
    id_propietario: UUID
    nombre: str
    edad: int
    tipo_mascota: str
    raza: Optional[str] = None
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None
    id_usuario_creacion: UUID
    id_usuario_edita: Optional[UUID] = None


@router.get("", response_model=List[MascotaRead])
def listar_mascotas() -> List[MascotaRead]:
    return crud_mascota.obtener_todos()


@router.get("/{id_mascota}", response_model=MascotaRead)
def obtener_mascota(id_mascota: UUID) -> MascotaRead:
    mascota = crud_mascota.obtener_por_id(id_mascota)
    if not mascota:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada"
        )
    return mascota
