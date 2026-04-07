from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import BaseModel
from src.database.config import get_db
from src.crud import vacuna as crud_v
from src.crud import mascota as crud_m
from src.crud import usuario as crud_u

router = APIRouter()


class VacunaCreate(BaseModel):
    nombre: str
    costo: float
    id_mascota: UUID
    id_usuario_registra: UUID


class VacunaUpdate(BaseModel):
    nombre: str | None = None
    costo: float | None = None


@router.get("/vacunas")
def listar_vacunas(db: Session = Depends(get_db)):
    return crud_v.obtener_todos()


@router.get("/vacunas/{vacuna_id}")
def obtener_vacuna(vacuna_id: UUID, db: Session = Depends(get_db)):
    vacuna = crud_v.obtener_por_id(vacuna_id)
    if not vacuna:
        raise HTTPException(status_code=404, detail="Vacuna no encontrada")
    return vacuna


@router.get("/vacunas/mascota/{mascota_id}")
def listar_vacunas_por_mascota(mascota_id: UUID, db: Session = Depends(get_db)):
    mascota = crud_m.obtener_por_id(mascota_id)
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    return crud_v.obtener_por_mascota(mascota_id)


@router.post("/vacunas")
def crear_vacuna(vacuna: VacunaCreate, db: Session = Depends(get_db)):
    if not crud_m.obtener_por_id(vacuna.id_mascota):
        raise HTTPException(status_code=404, detail="Mascota no encontrada")
    if not crud_u.obtener_por_id(vacuna.id_usuario_registra):
        raise HTTPException(status_code=404, detail="Usuario registrador no encontrado")

    nueva = crud_v.crear(
        nombre=vacuna.nombre,
        costo=vacuna.costo,
        id_mascota=vacuna.id_mascota,
        id_usuario_registra=vacuna.id_usuario_registra,
    )
    return nueva


@router.put("/vacunas/{vacuna_id}")
def actualizar_vacuna(
    vacuna_id: UUID, vacuna: VacunaUpdate, db: Session = Depends(get_db)
):
    existente = crud_v.obtener_por_id(vacuna_id)
    if not existente:
        raise HTTPException(status_code=404, detail="Vacuna no encontrada")

    update_data = vacuna.model_dump(exclude_unset=True)
    actualizada = crud_v.actualizar(vacuna_id, **update_data)
    return actualizada


@router.delete("/vacunas/{vacuna_id}")
def eliminar_vacuna(vacuna_id: UUID, db: Session = Depends(get_db)):
    if not crud_v.eliminar(vacuna_id):
        raise HTTPException(status_code=404, detail="Vacuna no encontrada")
    return {"message": "Vacuna eliminada correctamente"}
