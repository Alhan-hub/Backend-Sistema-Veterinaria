from typing import List, Optional
from src.database.config import SessionLocal
from src.entities.usuario import Usuario

db = SessionLocal()


def crear(nombre: str, nombre_usuario: str, clave: str, email: str) -> Usuario:

    usuario = Usuario(
        nombre=nombre, nombre_usuario=nombre_usuario, clave=clave, email=email
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return usuario


def obtener_todos() -> List[Usuario]:
    return db.query(Usuario).all()


def obtener_por_id(id_usuario: int) -> Optional[Usuario]:
    return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()


def eliminar(id_usuario: int) -> bool:
    usuario = obtener_por_id(id_usuario)

    if not usuario:
        return False

    db.delete(usuario)
    db.commit()

    return True
