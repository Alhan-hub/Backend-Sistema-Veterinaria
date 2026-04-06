from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.entities.cita import Cita


def crear(
    db: Session,
    id_mascota: UUID,
    id_usuario_agenda: UUID,
    motivo: str,
    costo: float,
    lugar: Optional[str] = None,
) -> Cita:
    cita = Cita(
        id_mascota=id_mascota,
        id_usuario_agenda=id_usuario_agenda,
        motivo=motivo.strip(),
        costo=costo,
        lugar=lugar.strip() if lugar else None,
        estado="pendiente",
    )
    db.add(cita)
    db.commit()
    db.refresh(cita)
    return cita


def obtener(db: Session, id_cita: UUID) -> Optional[Cita]:
    return db.query(Cita).filter(Cita.id_cita == id_cita).first()


def listar(db: Session, skip: int = 0, limit: int = 100) -> List[Cita]:
    return db.query(Cita).offset(skip).limit(limit).all()


def actualizar(
    db: Session,
    id_cita: UUID,
    **kwargs,
) -> Optional[Cita]:
    cita = obtener(db, id_cita)
    if not cita:
        return None
    for key, value in kwargs.items():
        if hasattr(cita, str(key)) and str(key) != "id_cita":
            setattr(cita, str(key), value)
    db.commit()
    db.refresh(cita)
    return cita


def eliminar(db: Session, id_cita: UUID) -> bool:
    cita = obtener(db, id_cita)
    if not cita:
        return False
    db.delete(cita)
    db.commit()
    return True
