from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.propietario import Propietario

db = SessionLocal()

def crear(
    nombre: str,
    id_usuario_creacion: UUID,
    telefono: str,
    email: Optional[str] = None,
) -> Propietario:
    if not nombre.strip():
        raise ValueError("El nombre es obligatorio")
    propietario = Propietario(
        nombre=nombre.strip(),
        id_usuario_creacion=id_usuario_creacion,
        telefono=telefono.strip(),
        email=email.strip() if email else None,
    )
    db.add(propietario)
    db.commit()
    db.refresh(propietario)
    return propietario


def obtener_por_id(id_propietario: UUID) -> Optional[Propietario]:
    return db.query(Propietario).filter(Propietario.id_propietario == id_propietario).first()


def obtener_todos() -> List[Propietario]:
    return db.query(Propietario).all()


def actualizar(
    id_propietario: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict,
) -> Optional[Propietario]:
    propietario = obtener_por_id(id_propietario)
    if not propietario:
        return None
    for key, value in kwargs.items():
        if hasattr(propietario, key):
            setattr(propietario, key, value)
    propietario.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(propietario)
    return propietario


def eliminar(id_propietario: UUID) -> bool:
    propietario = obtener_por_id(id_propietario)
    if not propietario:
        return False
    db.delete(propietario)
    db.commit()
    return True