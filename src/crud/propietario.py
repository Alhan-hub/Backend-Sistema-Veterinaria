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
    propietario = Propietario(
        nombre=nombre.strip(),
        id_usuario_creacion=id_usuario_creacion,
        telefono = telefono.strip()
        email=email.strip() if email else None,
    )
    db.add(propietario)
    db.commit()
    db.refresh(propietario)
    return propietario
