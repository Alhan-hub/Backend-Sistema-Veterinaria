"""
Endpoints para la entidad Factura.
"""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from src.database.config import get_db
from src.crud import factura as crud_factura

router = APIRouter(prefix="/facturas", tags=["facturas"])


class FacturaCreate(BaseModel):
    id_cita: UUID
    id_propietario: UUID
    id_usuario_genera: UUID
    total: float
    metodo_pago: str


class FacturaUpdate(BaseModel):
    total: Optional[float] = None
    metodo_pago: Optional[str] = None


class FacturaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_factura: UUID
    id_cita: UUID
    id_propietario: UUID
    id_usuario_genera: UUID
    total: float
    metodo_pago: str
    fecha_pago: datetime


@router.get("", response_model=List[FacturaRead])
def listar_facturas(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> List[FacturaRead]:
    return crud_factura.listar(db, skip=skip, limit=limit)


@router.get("/{id_factura}", response_model=FacturaRead)
def obtener_factura(id_factura: UUID, db: Session = Depends(get_db)) -> FacturaRead:
    f = crud_factura.obtener(db, id_factura)
    if not f:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
        )
    return f


@router.post("", response_model=FacturaRead, status_code=status.HTTP_201_CREATED)
def crear_factura(body: FacturaCreate, db: Session = Depends(get_db)) -> FacturaRead:
    try:
        return crud_factura.crear(
            db=db,
            id_cita=body.id_cita,
            id_propietario=body.id_propietario,
            id_usuario_genera=body.id_usuario_genera,
            total=body.total,
            metodo_pago=body.metodo_pago,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id_factura}", response_model=FacturaRead)
def actualizar_factura(
    id_factura: UUID, body: FacturaUpdate, db: Session = Depends(get_db)
) -> FacturaRead:
    data = body.model_dump(exclude_unset=True)
    f = crud_factura.actualizar(db, id_factura, **data)
    if not f:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
        )
    return f


@router.delete("/{id_factura}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_factura(id_factura: UUID, db: Session = Depends(get_db)) -> None:
    if not crud_factura.eliminar(db, id_factura):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada"
        )
