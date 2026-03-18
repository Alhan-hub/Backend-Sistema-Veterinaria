import uuid

from sqlalchemy import Column, DateTime, String, Numeric, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class Factura(Base):
    """
    Modelo de factura veterinaria.

    Representa el comprobante de pago generado a partir de una cita.
    Cada factura esta asociada a una cita especifica y es generada por un usuario del sistema.
    """

    __tablename__ = "factura"

    id_factura = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_cita = Column(
        UUID(as_uuid=True), ForeignKey("cita.id_cita"), nullable=False, unique=True
    )
    id_propietario = Column(
        UUID(as_uuid=True), ForeignKey("propietario.id_propietario"), nullable=False
    )
    id_usuario_genera = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )

    total = Column(Numeric(10, 2), nullable=False)
    metodo_pago = Column(String(50))
    fecha_pago = Column(DateTime(timezone=True), server_default=func.now())
