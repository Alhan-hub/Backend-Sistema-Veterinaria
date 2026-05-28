import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.crud.vacuna import crear as crear_vacuna, eliminar as eliminar_vacuna
from src.crud.mascota import crear as crear_mascota
from src.crud.usuario import crear as crear_usuario
from src.crud.propietario import crear as crear_propietario


def crear_mascota_aux(db_session: Session) -> tuple[str, str]:
    usuario = crear_usuario(
        nombre="Test",
        nombre_usuario=f"test_{uuid.uuid4().hex[:8]}",
        email=f"test_{uuid.uuid4().hex[:8]}@test.com",
        clave="1234",
    )
    propietario = crear_propietario(
        nombre="Dueño Test",
        id_usuario_creacion=usuario.id_usuario,
        telefono="123456",
    )
    mascota = crear_mascota(
        nombre="Firulais",
        id_propietario=propietario.id_propietario,
        id_usuario_creacion=usuario.id_usuario,
        edad=2,
        tipo_mascota="Perro",
    )
    return mascota.id_mascota, usuario.id_usuario


def test_listar_vacunas_error_ruta_incorrecta(client: TestClient) -> None:
    res = client.get("/vacuna/")
    assert res.status_code == 404


def test_listar_vacunas(client: TestClient) -> None:
    res = client.get("/vacunas/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_obtener_vacuna_inexistente_404(client: TestClient) -> None:
    res = client.get(f"/vacunas/{uuid.uuid4()}")
    assert res.status_code == 404


def test_obtener_vacuna_existente(client: TestClient, db_session: Session) -> None:
    id_mascota, id_usuario = crear_mascota_aux(db_session)
    vacuna = crear_vacuna(
        nombre="Rabia",
        costo=75.50,
        id_mascota=id_mascota,
        id_usuario_registra=id_usuario,
    )
    res = client.get(f"/vacunas/{vacuna.id_vacuna}")
    assert res.status_code == 200
    eliminar_vacuna(db_session, vacuna.id_vacuna)


def test_crear_vacuna(client: TestClient, db_session: Session) -> None:
    id_mascota, id_usuario = crear_mascota_aux(db_session)
    res = client.post(
        "/vacunas/",
        json={
            "nombre": "Parvovirus",
            "costo": 60.00,
            "id_mascota": str(id_mascota),
            "id_usuario_registra": str(id_usuario),
        },
    )
    assert res.status_code == 201


def test_crear_vacuna_error_datos_invalidos(client: TestClient) -> None:
    res = client.post("/vacunas/", json={"nombre": "Incompleta"})
    assert res.status_code == 422


def test_crear_vacuna_mascota_no_existe(client: TestClient) -> None:
    res = client.post(
        "/vacunas/",
        json={
            "nombre": "Rabia",
            "costo": 75.50,
            "id_mascota": str(uuid.uuid4()),
            "id_usuario_registra": str(uuid.uuid4()),
        },
    )
    assert res.status_code == 404


def test_obtener_vacunas_por_mascota(client: TestClient, db_session: Session) -> None:
    id_mascota, id_usuario = crear_mascota_aux(db_session)
    vacuna = crear_vacuna(
        nombre="Moquillo",
        costo=80.00,
        id_mascota=id_mascota,
        id_usuario_registra=id_usuario,
    )
    res = client.get(f"/vacunas/mascota/{id_mascota}")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    eliminar_vacuna(db_session, vacuna.id_vacuna)


def test_obtener_vacunas_por_mascota_inexistente(client: TestClient) -> None:
    res = client.get(f"/vacunas/mascota/{uuid.uuid4()}")
    assert res.status_code == 404


def test_editar_vacuna_inexistente_404(client: TestClient) -> None:
    res = client.put(
        f"/vacunas/{uuid.uuid4()}",
        json={"costo": 100.00},
    )
    assert res.status_code == 404


def test_editar_vacuna_existente(client: TestClient, db_session: Session) -> None:
    id_mascota, id_usuario = crear_mascota_aux(db_session)
    vacuna = crear_vacuna(
        nombre="Antes",
        costo=50.00,
        id_mascota=id_mascota,
        id_usuario_registra=id_usuario,
    )
    res = client.put(
        f"/vacunas/{vacuna.id_vacuna}",
        json={"costo": 120.00},
    )
    assert res.status_code == 200
    eliminar_vacuna(db_session, vacuna.id_vacuna)


def test_eliminar_vacuna_inexistente_404(client: TestClient) -> None:
    res = client.delete(f"/vacunas/{uuid.uuid4()}")
    assert res.status_code == 404


def test_eliminar_vacuna_existente(client: TestClient, db_session: Session) -> None:
    id_mascota, id_usuario = crear_mascota_aux(db_session)
    vacuna = crear_vacuna(
        nombre="Para eliminar",
        costo=30.00,
        id_mascota=id_mascota,
        id_usuario_registra=id_usuario,
    )
    res = client.delete(f"/vacunas/{vacuna.id_vacuna}")
    assert res.status_code == 204
