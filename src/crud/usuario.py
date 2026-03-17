from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
import src.entities.usuario


def crear(
    nombre: str, nombre_usuario: str, clave: str, email: str
) -> src.entities.usuario.Usuario:
    db = SessionLocal()
    usuario = src.entities.usuario.Usuario(
        nombre=nombre,
        nombre_usuario=nombre_usuario,
        clave=clave,
        email=email,
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    db.close()
    return usuario


def obtener_por_id(id_usuario: UUID) -> Optional[src.entities.usuario.Usuario]:
    db = SessionLocal()
    usuario = (
        db.query(src.entities.usuario.Usuario)
        .filter(src.entities.usuario.Usuario.id_usuario == id_usuario)
        .first()
    )
    db.close()
    return usuario


def obtener_todos() -> List[src.entities.usuario.Usuario]:
    db = SessionLocal()
    usuarios = db.query(src.entities.usuario.Usuario).all()
    db.close()
    return usuarios


def obtener_por_nombre_usuario(
    nombre_usuario: str,
) -> Optional[src.entities.usuario.Usuario]:
    db = SessionLocal()
    usuario = (
        db.query(src.entities.usuario.Usuario)
        .filter(src.entities.usuario.Usuario.nombre_usuario == nombre_usuario)
        .first()
    )
    db.close()
    return usuario


def actualizar(id_usuario: UUID, **kwargs) -> Optional[src.entities.usuario.Usuario]:
    db = SessionLocal()
    usuario = (
        db.query(src.entities.usuario.Usuario)
        .filter(src.entities.usuario.Usuario.id_usuario == id_usuario)
        .first()
    )

    if not usuario:
        db.close()
        return None

    for key, value in kwargs.items():
        if hasattr(usuario, key):
            setattr(usuario, key, value)

    db.commit()
    db.refresh(usuario)
    db.close()
    return usuario


def eliminar(id_usuario: UUID) -> bool:
    db = SessionLocal()
    usuario = (
        db.query(src.entities.usuario.Usuario)
        .filter(src.entities.usuario.Usuario.id_usuario == id_usuario)
        .first()
    )

    if not usuario:
        db.close()
        return False

    db.delete(usuario)
    db.commit()
    db.close()
    return True
