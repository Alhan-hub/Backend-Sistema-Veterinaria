import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.crud.factura import crear, eliminar as eliminar_factura
from src.crud.cita import crear as crear_cita
from src.crud.mascota import crear as crear_mascota
from src.crud.usuario import crear as crear_usuario
from src.crud.propietario import crear as crear_propietario


def crear_cita_aux(db_session: Session) -> tuple[str, str, str]:
    """Crea una cita con sus dependencias auxiliares."""
    # Usuario
    usuario = crear_usuario(
        db_session,
        nombre="Test",
        nombre_usuario=f"test_{uuid.uuid4().hex[:8]}",
        email=f"test_{uuid.uuid4().hex[:8]}@test.com",
        clave="1234",
    )
    # Propietario
    propietario = crear_propietario(
        db_session,
        nombre="Dueño Test",
        telefono="123456",
        id_usuario_creacion=usuario.id_usuario,
    )
    # Mascota
    mascota = crear_mascota(
        db_session,
        nombre="Firulais",
        id_propietario=propietario.id_propietario,
        id_usuario_creacion=usuario.id_usuario,
        edad=2,
        tipo_mascota="Perro",
    )
    # Cita
    cita = crear_cita(
        db_session,
        id_mascota=mascota.id_mascota,
        id_usuario_agenda=usuario.id_usuario,
        motivo="Consulta general",
        costo=50.0,
    )
    return cita.id_cita, propietario.id_propietario, usuario.id_usuario


def test_listar_facturas_error_ruta_incorrecta(client: TestClient) -> None:
    res = client.get("/factura/")
    assert res.status_code == 404


def test_listar_facturas(client: TestClient) -> None:
    res = client.get("/facturas/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_obtener_factura_inexistente_404(client: TestClient) -> None:
    res = client.get(f"/facturas/{uuid.uuid4()}")
    assert res.status_code == 404


def test_obtener_factura_existente(client: TestClient, db_session: Session) -> None:
    id_cita, id_propietario, id_usuario = crear_cita_aux(db_session)
    factura = crear(
        db_session,
        id_cita=id_cita,
        id_propietario=id_propietario,
        id_usuario_genera=id_usuario,
        total=100.0,
        metodo_pago="Efectivo",
    )
    res = client.get(f"/facturas/{factura.id_factura}")
    assert res.status_code == 200
    eliminar_factura(db_session, factura.id_factura)


def test_crear_factura(client: TestClient, db_session: Session) -> None:
    id_cita, id_propietario, id_usuario = crear_cita_aux(db_session)
    res = client.post(
        "/facturas/",
        json={
            "id_cita": str(id_cita),
            "id_propietario": str(id_propietario),
            "id_usuario_genera": str(id_usuario),
            "total": 150.0,
            "metodo_pago": "Tarjeta",
        },
    )
    assert res.status_code == 201


def test_crear_factura_error_datos_invalidos(client: TestClient) -> None:
    res = client.post("/facturas/", json={"total": "texto_invalido"})
    assert res.status_code == 422


def test_editar_factura_inexistente_404(client: TestClient) -> None:
    res = client.put(
        f"/facturas/{uuid.uuid4()}",
        json={"total": 200.0},
    )
    assert res.status_code == 404


def test_editar_factura_existente(client: TestClient, db_session: Session) -> None:
    id_cita, id_propietario, id_usuario = crear_cita_aux(db_session)
    factura = crear(
        db_session,
        id_cita=id_cita,
        id_propietario=id_propietario,
        id_usuario_genera=id_usuario,
        total=100.0,
        metodo_pago="Efectivo",
    )
    res = client.put(
        f"/facturas/{factura.id_factura}",
        json={"total": 250.0},
    )
    assert res.status_code == 200
    eliminar_factura(db_session, factura.id_factura)


def test_eliminar_factura_inexistente_404(client: TestClient) -> None:
    res = client.delete(f"/facturas/{uuid.uuid4()}")
    assert res.status_code == 404


def test_eliminar_factura_existente(client: TestClient, db_session: Session) -> None:
    id_cita, id_propietario, id_usuario = crear_cita_aux(db_session)
    factura = crear(
        db_session,
        id_cita=id_cita,
        id_propietario=id_propietario,
        id_usuario_genera=id_usuario,
        total=100.0,
        metodo_pago="Efectivo",
    )
    res = client.delete(f"/facturas/{factura.id_factura}")
    assert res.status_code == 204
