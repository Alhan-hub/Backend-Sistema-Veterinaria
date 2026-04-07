from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import BaseModel
from src.database.config import get_db
from src.crud import usuario as crud_u

router = APIRouter()


class UsuarioCreate(BaseModel):
    nombre: str
    nombre_usuario: str
    clave: str
    email: str


class UsuarioUpdate(BaseModel):
    nombre: str | None = None
    nombre_usuario: str | None = None
    clave: str | None = None
    email: str | None = None


@router.get("/usuarios")
def listar_usuarios(db: Session = Depends(get_db)):
    return crud_u.obtener_todos()


@router.get("/usuarios/{usuario_id}")
def obtener_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    usuario = crud_u.obtener_por_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.post("/usuarios")
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if crud_u.existe_nombre_usuario(usuario.nombre_usuario):
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")
    if crud_u.existe_email(usuario.email):
        raise HTTPException(status_code=400, detail="El email ya existe")

    nuevo = crud_u.crear(
        nombre=usuario.nombre,
        nombre_usuario=usuario.nombre_usuario,
        clave=usuario.clave,
        email=usuario.email,
    )
    return nuevo


@router.put("/usuarios/{usuario_id}")
def actualizar_usuario(
    usuario_id: UUID, usuario: UsuarioUpdate, db: Session = Depends(get_db)
):
    existente = crud_u.obtener_por_id(usuario_id)
    if not existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    update_data = usuario.model_dump(exclude_unset=True)
    actualizado = crud_u.actualizar(usuario_id, **update_data)
    return actualizado


@router.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    if not crud_u.eliminar(usuario_id):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado correctamente"}
