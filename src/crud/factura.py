from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.entities.factura import Factura


def crear(
    db: Session,
    id_cita: UUID,
    id_propietario: UUID,
    id_usuario_genera: UUID,
    total: float,
    metodo_pago: str,
) -> Factura:
    factura_existente = db.query(Factura).filter(Factura.id_cita == id_cita).first()
    if factura_existente:
        raise ValueError("La cita ya tiene una factura asociada")
    factura = Factura(
        id_cita=id_cita,
        id_propietario=id_propietario,
        id_usuario_genera=id_usuario_genera,
        total=total,
        metodo_pago=metodo_pago.strip(),
    )
    db.add(factura)
    db.commit()
    db.refresh(factura)
    return factura


def obtener(db: Session, id_factura: UUID) -> Optional[Factura]:
    return db.query(Factura).filter(Factura.id_factura == id_factura).first()


def listar(db: Session, skip: int = 0, limit: int = 100) -> List[Factura]:
    return db.query(Factura).offset(skip).limit(limit).all()


def actualizar(
    db: Session,
    id_factura: UUID,
    **kwargs,
) -> Optional[Factura]:
    factura = obtener(db, id_factura)
    if not factura:
        return None
    for key, value in kwargs.items():
        if hasattr(factura, str(key)) and str(key) != "id_factura":
            setattr(factura, str(key), value)
    db.commit()
    db.refresh(factura)
    return factura


def eliminar(db: Session, id_factura: UUID) -> bool:
    factura = obtener(db, id_factura)
    if not factura:
        return False
    db.delete(factura)
    db.commit()
    return True
