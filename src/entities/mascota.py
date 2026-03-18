import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.database.config import Base


class Mascota(Base):
    """Modelo de Mascota"""

    __tablename__ = "mascota"

    id_mascota = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_propietario = Column(
        UUID(as_uuid=True), ForeignKey("propietario.id_propietario"), nullable=False
    )

    nombre = Column(Text, nullable=False)
    edad = Column(Integer, nullable=False)
    tipo_mascota = Column(Text, nullable=False)
    raza = Column(Text, nullable=True)
   
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )

    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])
    propietario = relationship("Propietario", foreign_keys=[id_propietario])