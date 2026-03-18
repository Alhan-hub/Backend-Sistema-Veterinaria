from typing import List, Optional
from uuid import UUID

from src.database.config import SessionLocal
from src.entities.factura import Factura

db = SessionLocal()


def crear(
    id_cita: UUID,
    id_propietario: UUID,
    id_usuario_genera: UUID,
    total: float,
    metodo_pago: str,
) -> Factura:
    """
    Crea una nueva factura en la base de datos.
    """
    factura_existente = db.query(Factura).filter(Factura.id_cita == id_cita).first()
    if factura_existente:
        raise ValueError("La cita ya tiene una factura asociada")

    factura = Factura(
        id_cita=id_cita,
        id_propietario=id_propietario,
        id_usuario_genera=id_usuario_genera,
        total=total,
        metodo_pago=metodo_pago.strip(),
    )
    db.add(factura)
    db.commit()
    db.refresh(factura)
    return factura


def obtener_por_id(id_factura: UUID) -> Optional[Factura]:
    """
    Retorna una factura por su ID.
    """
    return db.query(Factura).filter(Factura.id_factura == id_factura).first()


def obtener_todos() -> List[Factura]:
    """
    Retorna todas las facturas.
    """
    return db.query(Factura).all()


def obtener_por_cita(id_cita: UUID) -> Optional[Factura]:
    """
    Retorna la factura asociada a una cita especifica.
    """
    return db.query(Factura).filter(Factura.id_cita == id_cita).first()


def obtener_por_propietario(id_propietario: UUID) -> List[Factura]:
    """
    Retorna todas las facturas de un propietario especifico.
    """
    return db.query(Factura).filter(Factura.id_propietario == id_propietario).all()


def obtener_por_usuario(id_usuario_genera: UUID) -> List[Factura]:
    """
    Retorna todas las facturas generadas por un usuario especifico.
    """
    return (
        db.query(Factura).filter(Factura.id_usuario_genera == id_usuario_genera).all()
    )


def actualizar(
    id_factura: UUID,
    **kwargs: dict,
) -> Optional[Factura]:
    """
    Actualiza los campos de una factura existente.
    """
    factura = obtener_por_id(id_factura)
    if not factura:
        return None

    for key, value in kwargs.items():
        if hasattr(factura, key):
            if isinstance(value, str):
                value = value.strip()
            setattr(factura, key, value)

    db.commit()
    db.refresh(factura)
    return factura


def eliminar(id_factura: UUID) -> bool:
    """
    Elimina una factura de la base de datos.
    """
    factura = obtener_por_id(id_factura)
    if not factura:
        return False

    db.delete(factura)
    db.commit()
    return True
