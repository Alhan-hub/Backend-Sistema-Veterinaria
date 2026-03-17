import uuid

from sqlalchemy import Column, DateTime, String, Numeric, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class Cita(Base):
    """
    Modelo de cita veterinaria.

    Representa una consulta agendada para una mascota.
    Cada cita está asociada a una mascota y es registrada por un usuario.
    """

    __tablename__ = "cita"

    id_cita = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_mascota = Column(
        UUID(as_uuid=True), ForeignKey("mascota.id_mascota"), nullable=False
    )
    id_usuario_agenda = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )

    fecha_hora = Column(DateTime(timezone=True), server_default=func.now())
    lugar = Column(String(100))
    motivo = Column(String(255))
    costo = Column(Numeric(10, 2))
    estado = Column(String(20), default="pendiente")
