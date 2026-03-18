import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from src.database.config import Base


class Usuario(Base):
    """
    Modelo de usuario del sistema.

    Atributos:
        id_usuario: Identificador único del usuario (UUID)
        nombre: Nombre completo del usuario
        nombre_usuario: Nombre de usuario para login (único)
        clave: Contraseña hasheada del usuario
        email: Correo electrónico del usuario (único)
        created_at: Fecha y hora de creación
        updated_at: Fecha y hora de última actualización
        created_by: Usuario que creó el registro
        updated_by: Último usuario que actualizó
    """

    __tablename__ = "usuario"

    id_usuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), nullable=False)
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    clave = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=False,
    )
    created_by = Column(UUID(as_uuid=True), nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)
