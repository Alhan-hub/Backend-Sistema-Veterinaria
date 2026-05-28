
import uuid

from fastapi.testclient import TestClient

from src.crud.usuario import crear as crear_usuario
from src.crud.propietario import crear as crear_propietario
from src.crud.mascota import (
    crear,
    eliminar,
)

def crear_mascota_aux():

    usuario = crear_usuario(
        nombre="Usuario Test",
        nombre_usuario=f"user_{uuid.uuid4().hex[:8]}",
        email=f"user_{uuid.uuid4().hex[:8]}@test.com",
        clave="1234",
    )

    propietario = crear_propietario(
        nombre="Propietario Test",
        telefono="3001234567",
        email=f"prop_{uuid.uuid4().hex[:8]}@test.com",
        id_usuario_creacion=usuario.id_usuario,
    )

    mascota = crear(
        nombre="Firulais",
        id_propietario=propietario.id_propietario,
        id_usuario_creacion=usuario.id_usuario,
        edad=5,
        tipo_mascota="Perro",
        raza="Labrador",
    )

    return mascota, usuario, propietario

def test_listar_mascotas(client: TestClient):

    res = client.get("/mascotas")

    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_listar_mascotas_ruta_incorrecta(client: TestClient):

    res = client.get("/mascota")

    assert res.status_code == 404


def test_obtener_mascota_existente(client: TestClient):

    mascota, usuario, propietario = crear_mascota_aux()

    res = client.get(f"/mascotas/{mascota.id_mascota}")

    assert res.status_code == 200
    assert res.json()["nombre"] == "Firulais"

    eliminar(mascota.id_mascota)


def test_obtener_mascota_inexistente(client: TestClient):

    res = client.get(f"/mascotas/{uuid.uuid4()}")

    assert res.status_code == 404


def test_crear_mascota(client: TestClient):

    usuario = crear_usuario(
        nombre="Usuario Crear",
        nombre_usuario=f"user_{uuid.uuid4().hex[:8]}",
        email=f"crear_{uuid.uuid4().hex[:8]}@test.com",
        clave="1234",
    )

    propietario = crear_propietario(
        nombre="Carlos",
        telefono="3112223344",
        email=f"carlos_{uuid.uuid4().hex[:8]}@test.com",
        id_usuario_creacion=usuario.id_usuario,
    )

    res = client.post(
        "/mascotas",
        json={
            "nombre": "Max",
            "id_propietario": str(propietario.id_propietario),
            "id_usuario_creacion": str(usuario.id_usuario),
            "edad": 3,
            "tipo_mascota": "Perro",
            "raza": "Golden",
        },
    )

    assert res.status_code == 201
    assert res.json()["nombre"] == "Max"


def test_crear_mascota_error_datos_invalidos(client: TestClient):

    res = client.post(
        "/mascotas",
        json={
            "nombre": "Error"
        },
    )

    assert res.status_code == 422

def test_actualizar_mascota_existente(client: TestClient):

    mascota, usuario, propietario = crear_mascota_aux()

    res = client.put(
        f"/mascotas/{mascota.id_mascota}",
        json={
            "nombre": "Rocky",
            "edad": 7,
            "tipo_mascota": "Perro",
            "raza": "Pastor Alemán",
            "id_usuario_edita": str(usuario.id_usuario),
        },
    )

    assert res.status_code == 200
    assert res.json()["nombre"] == "Rocky"

    eliminar(mascota.id_mascota)


def test_actualizar_mascota_inexistente(client: TestClient):

    res = client.put(
        f"/mascotas/{uuid.uuid4()}",
        json={
            "nombre": "Fantasma",
            "id_usuario_edita": str(uuid.uuid4()),
        },
    )

    assert res.status_code == 404

def test_eliminar_mascota_existente(client: TestClient):

    mascota, usuario, propietario = crear_mascota_aux()

    res = client.delete(f"/mascotas/{mascota.id_mascota}")

    assert res.status_code == 204


def test_eliminar_mascota_inexistente(client: TestClient):

    res = client.delete(f"/mascotas/{uuid.uuid4()}")

    assert res.status_code == 404
