from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
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
