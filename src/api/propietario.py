from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from .deps import DbSession
from src.crud import pedido as crud_pedido

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
