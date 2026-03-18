from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.entities.vacuna import Vacuna

db = SessionLocal()


def crear(
    nombre: str, costo: float, id_mascota: UUID, id_usuario_registra: UUID
) -> Optional[Vacuna]:
    vacuna = Vacuna(
        nombre=nombre.strip(),
        costo=costo,
        id_mascota=id_mascota,
        id_usuario_registra=id_usuario_registra,
    )
    db.add(vacuna)
    db.commit()
    db.refresh(vacuna)
    return vacuna


def obtener_por_id(id_vacuna: UUID) -> Optional[Vacuna]:
    return db.query(Vacuna).filter(Vacuna.id_vacuna == id_vacuna).first()


def obtener_todos() -> List[Vacuna]:
    return db.query(Vacuna).all()


def obtener_por_mascota(id_mascota: UUID) -> List[Vacuna]:
    return db.query(Vacuna).filter(Vacuna.id_mascota == id_mascota).all()


def actualizar(id_vacuna: UUID, **kwargs) -> Optional[Vacuna]:
    vacuna = obtener_por_id(id_vacuna)
    if not vacuna:
        return None

    for key, value in kwargs.items():
        if hasattr(vacuna, key) and value is not None:
            if key == "nombre":
                value = value.strip()
            setattr(vacuna, key, value)

    db.commit()
    db.refresh(vacuna)
    return vacuna


def eliminar(id_vacuna: UUID) -> bool:
    vacuna = obtener_por_id(id_vacuna)
    if not vacuna:
        return False
    db.delete(vacuna)
    db.commit()
    return True


def existe_vacuna_para_mascota(id_mascota: UUID, nombre: str) -> bool:
    nombre = nombre.strip()
    return (
        db.query(Vacuna)
        .filter(Vacuna.id_mascota == id_mascota, Vacuna.nombre == nombre)
        .first()
        is not None
    )
