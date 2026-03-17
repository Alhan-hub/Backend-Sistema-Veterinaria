from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.mascota import Mascota

db = SessionLocal()

def crear(
    nombre: str,
    id_propietario: UUID,
    id_usuario_creacion: UUID,
    edad: int,
    tipo_mascota:str,
    raza: Optional[str] = None,
) -> Mascota:
    if not nombre.strip():
        raise ValueError("El nombre es obligatorio")
    mascota = Mascota(
        nombre=nombre.strip(),
        id_propietario=id_propietario,
        id_usuario_creacion=id_usuario_creacion,
        edad=edad,
        tipo_mascota=tipo_mascota.strip(),
        raza=raza.strip() if raza else None,
    )
    db.add(mascota)
    db.commit()
    db.refresh(mascota)
    return mascota
