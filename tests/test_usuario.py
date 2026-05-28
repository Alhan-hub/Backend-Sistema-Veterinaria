import uuid

from fastapi.testclient import TestClient

from src.crud.usuario import crear as crear_usuario, eliminar as eliminar_usuario


def test_listar_usuarios_error_ruta_incorrecta(client: TestClient) -> None:
    res = client.get("/usuario/")
    assert res.status_code == 404


def test_listar_usuarios(client: TestClient) -> None:
    res = client.get("/usuarios/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_obtener_usuario_inexistente_404(client: TestClient) -> None:
    res = client.get(f"/usuarios/{uuid.uuid4()}")
    assert res.status_code == 404


def test_obtener_usuario_existente(client: TestClient) -> None:
    usuario = crear_usuario(
        nombre="Test User",
        nombre_usuario=f"test_{uuid.uuid4().hex[:8]}",
        email=f"test_{uuid.uuid4().hex[:8]}@test.com",
        clave="1234",
    )
    res = client.get(f"/usuarios/{usuario.id_usuario}")
    assert res.status_code == 200
    eliminar_usuario(usuario.id_usuario)


def test_crear_usuario(client: TestClient) -> None:
    res = client.post(
        "/usuarios/",
        json={
            "nombre": "Juan Perez",
            "nombre_usuario": f"juan_{uuid.uuid4().hex[:8]}",
            "clave": "123456",
            "email": f"juan_{uuid.uuid4().hex[:8]}@test.com",
        },
    )
    assert res.status_code == 200


def test_crear_usuario_error_datos_invalidos(client: TestClient) -> None:
    res = client.post("/usuarios/", json={"nombre": "Incompleto"})
    assert res.status_code == 422


def test_editar_usuario_inexistente_404(client: TestClient) -> None:
    res = client.put(
        f"/usuarios/{uuid.uuid4()}",
        json={"nombre": "Nuevo Nombre"},
    )
    assert res.status_code == 404


def test_editar_usuario_existente(client: TestClient) -> None:
    usuario = crear_usuario(
        nombre="Antes",
        nombre_usuario=f"edit_{uuid.uuid4().hex[:8]}",
        email=f"edit_{uuid.uuid4().hex[:8]}@test.com",
        clave="1234",
    )
    res = client.put(
        f"/usuarios/{usuario.id_usuario}",
        json={"nombre": "Despues"},
    )
    assert res.status_code == 200
    eliminar_usuario(usuario.id_usuario)


def test_eliminar_usuario_inexistente_404(client: TestClient) -> None:
    res = client.delete(f"/usuarios/{uuid.uuid4()}")
    assert res.status_code == 404


def test_eliminar_usuario_existente(client: TestClient) -> None:
    usuario = crear_usuario(
        nombre="Para eliminar",
        nombre_usuario=f"del_{uuid.uuid4().hex[:8]}",
        email=f"del_{uuid.uuid4().hex[:8]}@test.com",
        clave="1234",
    )
    res = client.delete(f"/usuarios/{usuario.id_usuario}")
    assert res.status_code == 200
