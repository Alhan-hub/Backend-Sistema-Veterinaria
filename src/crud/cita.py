from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.cita import Cita

db = SessionLocal()


def crear(
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


def obtener_por_id(id_cita: UUID) -> Optional[Cita]:
    return db.query(Cita).filter(Cita.id_cita == id_cita).first()


def obtener_todos() -> List[Cita]:
    return db.query(Cita).all()


def obtener_por_mascota(id_mascota: UUID) -> List[Cita]:
    return db.query(Cita).filter(Cita.id_mascota == id_mascota).all()


def obtener_por_usuario(id_usuario_agenda: UUID) -> List[Cita]:
    return db.query(Cita).filter(Cita.id_usuario_agenda == id_usuario_agenda).all()


def actualizar(
    id_cita: UUID,
    **kwargs: dict,
) -> Optional[Cita]:
    cita = obtener_por_id(id_cita)
    if not cita:
        return None

    for key, value in kwargs.items():
        if hasattr(cita, key):
            # Aplicar strip() si es string
            if isinstance(value, str):
                value = value.strip()
            setattr(cita, key, value)

    db.commit()
    db.refresh(cita)
    return cita


def eliminar(id_cita: UUID) -> bool:
    cita = obtener_por_id(id_cita)
    if not cita:
        return False

    db.delete(cita)
    db.commit()
    return True
