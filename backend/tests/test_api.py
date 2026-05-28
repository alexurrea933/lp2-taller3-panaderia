from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_obtener_clientes():
    response = client.get("/clientes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert all("nombre" in cliente for cliente in response.json())


def test_crear_cliente():
    payload = {
        "nombre": "Cliente Prueba",
        "telefono": "3001231234",
        "correo": "prueba@mail.com",
    }
    response = client.post("/clientes", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == payload["nombre"]
    assert data["telefono"] == payload["telefono"]
    assert data["correo"] == payload["correo"]
    assert isinstance(data["id"], int)


def test_obtener_cliente_por_id():
    clientes_resp = client.get("/clientes")
    assert clientes_resp.status_code == 200
    clientes = clientes_resp.json()
    assert len(clientes) > 0

    cliente_id = clientes[0]["id"]
    response = client.get(f"/clientes/{cliente_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == cliente_id
    assert "nombre" in data


def test_obtener_pedidos_lista():
    response = client.get("/pedidos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_crear_pedido():
    clientes_resp = client.get("/clientes")
    assert clientes_resp.status_code == 200
    cliente_id = clientes_resp.json()[0]["id"]

    productos_resp = client.get("/productos")
    assert productos_resp.status_code == 200
    producto_id = productos_resp.json()[0]["id"]

    response = client.post(
        "/pedidos",
        json={
            "cliente_id": cliente_id,
            "detalles": [{"producto_id": producto_id, "cantidad": 1}],
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["cliente_id"] == cliente_id
    assert data["total"] > 0
    assert isinstance(data["detalles"], list)
    assert data["detalles"][0]["producto_id"] == producto_id
