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
    """
    Crea una nueva cita en la base de datos.
    """
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
    """
    Retorna una cita por su ID.
    """
    return db.query(Cita).filter(Cita.id_cita == id_cita).first()


def obtener_todos() -> List[Cita]:
    """
    Retorna todas las citas.
    """
    return db.query(Cita).all()


def obtener_por_mascota(id_mascota: UUID) -> List[Cita]:
    """
    Retorna todas las citas de una mascota especifica.
    """
    return db.query(Cita).filter(Cita.id_mascota == id_mascota).all()


def obtener_por_usuario(id_usuario_agenda: UUID) -> List[Cita]:
    """
    Retorna todas las citas agendadas por un usuario especifico.
    """
    return db.query(Cita).filter(Cita.id_usuario_agenda == id_usuario_agenda).all()


def actualizar(
    id_cita: UUID,
    **kwargs: dict,
) -> Optional[Cita]:
    """
    Actualiza los campos de una cita existente.

    Args:
        id_cita: UUID de la cita a actualizar
        **kwargs: Diccionario con los campos a actualizar

    Returns:
        Cita actualizada o None si no existe
    """
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
    """
    Elimina una cita de la base de datos.

    Returns:
        True si se elimino, False si no existia
    """
    cita = obtener_por_id(id_cita)
    if not cita:
        return False

    db.delete(cita)
    db.commit()
    return True
