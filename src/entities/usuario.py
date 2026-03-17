import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from src.database.config import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), nullable=False)
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    clave = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
