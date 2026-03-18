import uuid
from sqlalchemy import Column, String, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from src.database.config import Base


class Vacuna(Base):
    """
    Modelo de vacuna veterinaria.
    Representa una vacuna aplicada a una mascota.
    """

    __tablename__ = "vacuna"

    id_vacuna = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), nullable=False)
    costo = Column(Numeric(10, 2), nullable=False)
    id_mascota = Column(
        UUID(as_uuid=True), ForeignKey("mascota.id_mascota"), nullable=False
    )
    id_usuario_registra = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
