from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.entities.usuario import Usuario

db = SessionLocal()


def crear(
    nombre: str, nombre_usuario: str, clave: str, email: str
) -> Optional[Usuario]:
    if existe_nombre_usuario(nombre_usuario):
        print("Error: El nombre de usuario ya existe")
        return None
    if existe_email(email):
        print("Error: El email ya existe")
        return None

    usuario = Usuario(
        nombre=nombre.strip(),
        nombre_usuario=nombre_usuario.strip().lower(),
        clave=clave,
        email=email.strip().lower(),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def obtener_por_id(id_usuario: UUID) -> Optional[Usuario]:
    return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()


def obtener_todos() -> List[Usuario]:
    return db.query(Usuario).all()


def obtener_por_nombre_usuario(nombre_usuario: str) -> Optional[Usuario]:
    return (
        db.query(Usuario)
        .filter(Usuario.nombre_usuario == nombre_usuario.strip().lower())
        .first()
    )


def actualizar(id_usuario: UUID, **kwargs) -> Optional[Usuario]:
    usuario = obtener_por_id(id_usuario)
    if not usuario:
        return None

    for key, value in kwargs.items():
        if hasattr(usuario, key) and value is not None:
            if key in ["nombre", "nombre_usuario", "email"]:
                value = value.strip()
                if key in ["nombre_usuario", "email"]:
                    value = value.lower()
            setattr(usuario, key, value)

    db.commit()
    db.refresh(usuario)
    return usuario


def eliminar(id_usuario: UUID) -> bool:
    usuario = obtener_por_id(id_usuario)
    if not usuario:
        return False
    db.delete(usuario)
    db.commit()
    return True


def existe_nombre_usuario(nombre_usuario: str) -> bool:
    return (
        db.query(Usuario)
        .filter(Usuario.nombre_usuario == nombre_usuario.strip().lower())
        .first()
        is not None
    )


def existe_email(email: str) -> bool:
    return (
        db.query(Usuario).filter(Usuario.email == email.strip().lower()).first()
        is not None
    )
