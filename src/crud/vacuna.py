from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.entities.vacuna import Vacuna


def crear(
    nombre: str, costo: float, id_mascota: UUID, id_usuario_registra: UUID
) -> Optional[Vacuna]:
    db = SessionLocal()
    try:
        vacuna = Vacuna(
            nombre=nombre,
            costo=costo,
            id_mascota=id_mascota,
            id_usuario_registra=id_usuario_registra,
        )
        db.add(vacuna)
        db.commit()
        db.refresh(vacuna)
        return vacuna
    except:
        db.rollback()
        return None
    finally:
        db.close()


def obtener_por_id(id_vacuna: UUID) -> Optional[Vacuna]:
    db = SessionLocal()
    try:
        return db.query(Vacuna).filter(Vacuna.id_vacuna == id_vacuna).first()
    finally:
        db.close()


def obtener_todos() -> List[Vacuna]:
    db = SessionLocal()
    try:
        return db.query(Vacuna).all()
    finally:
        db.close()


def actualizar(id_vacuna: UUID, **kwargs) -> Optional[Vacuna]:
    db = SessionLocal()
    try:
        vacuna = db.query(Vacuna).filter(Vacuna.id_vacuna == id_vacuna).first()
        if not vacuna:
            return None
        for key, value in kwargs.items():
            if hasattr(vacuna, key):
                setattr(vacuna, key, value)
        db.commit()
        db.refresh(vacuna)
        return vacuna
    except:
        db.rollback()
        return None
    finally:
        db.close()


def eliminar(id_vacuna: UUID) -> bool:
    db = SessionLocal()
    try:
        vacuna = db.query(Vacuna).filter(Vacuna.id_vacuna == id_vacuna).first()
        if not vacuna:
            return False
        db.delete(vacuna)
        db.commit()
        return True
    except:
        db.rollback()
        return False
    finally:
        db.close()
