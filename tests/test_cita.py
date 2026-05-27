import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.crud.cita import crear, eliminar
from src.crud.mascota import crear as crear_mascota
from src.crud.usuario import crear as crear_usuario


def crear_mascota_aux(db_session: Session) -> tuple[str, str]:
    """Crea una mascota y un usuario auxiliares para las pruebas."""
    usuario = crear_usuario(
        db_session,
        nombre="Test",
        nombre_usuario=f"test_{uuid.uuid4().hex[:8]}",
        email=f"test_{uuid.uuid4().hex[:8]}@test.com",
        clave="1234",
    )
    mascota = crear_mascota(
        db_session,
        nombre="Firulais",
        id_propietario=uuid.uuid4(),
        id_usuario_creacion=usuario.id_usuario,
        edad=2,
        tipo_mascota="Perro",
    )
    return mascota.id_mascota, usuario.id_usuario


def test_listar_citas_error_ruta_incorrecta(client: TestClient) -> None:
    res = client.get("/cita/")
    assert res.status_code == 404


def test_listar_citas(client: TestClient) -> None:
    res = client.get("/citas/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_obtener_cita_inexistente_404(client: TestClient) -> None:
    res = client.get(f"/citas/{uuid.uuid4()}")
    assert res.status_code == 404


def test_obtener_cita_existente(client: TestClient, db_session: Session) -> None:
    id_mascota, id_usuario = crear_mascota_aux(db_session)
    cita = crear(
        db_session,
        id_mascota=id_mascota,
        id_usuario_agenda=id_usuario,
        motivo="Consulta general",
        costo=50.0,
    )
    res = client.get(f"/citas/{cita.id_cita}")
    assert res.status_code == 200
    eliminar(db_session, cita.id_cita)


def test_crear_cita(client: TestClient, db_session: Session) -> None:
    id_mascota, id_usuario = crear_mascota_aux(db_session)
    res = client.post(
        "/citas/",
        json={
            "id_mascota": str(id_mascota),
            "id_usuario_agenda": str(id_usuario),
            "motivo": "Vacunación",
            "costo": 75.0,
        },
    )
    assert res.status_code == 201


def test_crear_cita_error_datos_invalidos(client: TestClient) -> None:
    res = client.post("/citas/", json={"motivo": "Incompleto"})
    assert res.status_code == 422


def test_editar_cita_inexistente_404(client: TestClient) -> None:
    res = client.put(
        f"/citas/{uuid.uuid4()}",
        json={"estado": "realizada"},
    )
    assert res.status_code == 404


def test_editar_cita_existente(client: TestClient, db_session: Session) -> None:
    id_mascota, id_usuario = crear_mascota_aux(db_session)
    cita = crear(
        db_session,
        id_mascota=id_mascota,
        id_usuario_agenda=id_usuario,
        motivo="Consulta general",
        costo=50.0,
    )
    res = client.put(
        f"/citas/{cita.id_cita}",
        json={"estado": "realizada"},
    )
    assert res.status_code == 200
    eliminar(db_session, cita.id_cita)


def test_eliminar_cita_inexistente_404(client: TestClient) -> None:
    res = client.delete(f"/citas/{uuid.uuid4()}")
    assert res.status_code == 404


def test_eliminar_cita_existente(client: TestClient, db_session: Session) -> None:
    id_mascota, id_usuario = crear_mascota_aux(db_session)
    cita = crear(
        db_session,
        id_mascota=id_mascota,
        id_usuario_agenda=id_usuario,
        motivo="Consulta general",
        costo=50.0,
    )
    res = client.delete(f"/citas/{cita.id_cita}")
    assert res.status_code == 204
