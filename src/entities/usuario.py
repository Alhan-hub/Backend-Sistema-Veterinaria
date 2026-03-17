from sqlalchemy import Column, Integer, String
from src.database.config import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100))
    nombre_usuario = Column(String(50), unique=True)
    clave = Column(String(255))
    email = Column(String(100))
