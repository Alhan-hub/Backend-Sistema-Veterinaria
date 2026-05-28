
import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.crud.usuario import crear as crear_usuario
from src.crud.propietario import (
    crear,
    eliminar,
)

def crear_propietario_aux():
    usuario = crear_usuario(
        nombre="Usuario Test",
        nombre_usuario=f"user_{uuid.uuid4().hex[:8]}",
        email=f"test_{uuid.uuid4().hex[:8]}@test.com",
        clave="1234",
    )

    propietario = crear(
        nombre="Juan Perez",
        telefono="3001234567",
        email="juan@test.com",
        id_usuario_creacion=usuario.id_usuario,
    )

    return propietario, usuario

def test_listar_propietarios(client: TestClient):

    res = client.get("/propietarios")

    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_listar_propietarios_ruta_incorrecta(client: TestClient):

    res = client.get("/propietario")

    assert res.status_code == 404

def test_obtener_propietario_existente(client: TestClient):

    propietario, usuario = crear_propietario_aux()

    res = client.get(f"/propietarios/{propietario.id_propietario}")

    assert res.status_code == 200
    assert res.json()["nombre"] == "Juan Perez"

    eliminar(propietario.id_propietario)


def test_obtener_propietario_inexistente(client: TestClient):

    res = client.get(f"/propietarios/{uuid.uuid4()}")

    assert res.status_code == 404

def test_crear_propietario(client: TestClient):

    usuario = crear_usuario(
        nombre="Usuario Crear",
        nombre_usuario=f"user_{uuid.uuid4().hex[:8]}",
        email=f"crear_{uuid.uuid4().hex[:8]}@test.com",
        clave="1234",
    )

    res = client.post(
        "/propietarios",
        json={
            "nombre": "Carlos Lopez",
            "telefono": "3112223344",
            "email": "carlos@test.com",
            "id_usuario_creacion": str(usuario.id_usuario),
        },
    )

    assert res.status_code == 201
    assert res.json()["nombre"] == "Carlos Lopez"


def test_crear_propietario_error_datos_invalidos(client: TestClient):

    res = client.post(
        "/propietarios",
        json={
            "nombre": "Error"
        },
    )

    assert res.status_code == 422


def test_actualizar_propietario_existente(client: TestClient):

    propietario, usuario = crear_propietario_aux()

    res = client.put(
        f"/propietarios/{propietario.id_propietario}",
        json={
            "nombre": "Nuevo Nombre",
            "telefono": "3009998888",
            "id_usuario_edita": str(usuario.id_usuario),
        },
    )

    assert res.status_code == 200
    assert res.json()["nombre"] == "Nuevo Nombre"

    eliminar(propietario.id_propietario)


def test_actualizar_propietario_inexistente(client: TestClient):

    res = client.put(
        f"/propietarios/{uuid.uuid4()}",
        json={
            "nombre": "No Existe",
            "id_usuario_edita": str(uuid.uuid4()),
        },
    )

    assert res.status_code == 404

def test_eliminar_propietario_existente(client: TestClient):

    propietario, usuario = crear_propietario_aux()

    res = client.delete(f"/propietarios/{propietario.id_propietario}")

    assert res.status_code == 204


def test_eliminar_propietario_inexistente(client: TestClient):

    res = client.delete(f"/propietarios/{uuid.uuid4()}")

    assert res.status_code == 404
