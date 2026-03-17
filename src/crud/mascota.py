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


def obtener_por_id(id_mascota: UUID) -> Optional[Mascota]:
    return db.query(Mascota).filter(Mascota.id_mascota == id_mascota).first()


def obtener_todos() -> List[Mascota]:
    return db.query(Mascota).all()


def actualizar(
    id_mascota: UUID,
    id_usuario_edita: UUID,
    **kwargs: dict,
) -> Optional[Mascota]:
    mascota = obtener_por_id(id_mascota)
    if not mascota:
        return None
    for key, value in kwargs.items():
        if hasattr(mascota, key):
            setattr(mascota, key, value)
    mascota.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(mascota)
    return mascota

