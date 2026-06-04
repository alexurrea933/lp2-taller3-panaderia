import sys
import os

# Agregar el directorio backend al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_obtener_pedidos_lista():
    response = client.get("/api/pedidos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_crear_pedido():
    clientes_resp = client.get("/api/clientes")
    assert clientes_resp.status_code == 200
    cliente_id = clientes_resp.json()[0]["id"]

    productos_resp = client.get("/api/productos")
    assert productos_resp.status_code == 200
    producto_id = productos_resp.json()[0]["id"]

    response = client.post(
        "/api/pedidos",
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


def test_crear_pedido_con_cliente_inexistente():
    response = client.post(
        "/api/pedidos",
        json={
            "cliente_id": 999999,
            "detalles": [{"producto_id": 1, "cantidad": 1}],
        },
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente no encontrado"


def test_crear_pedido_con_producto_inexistente():
    clientes_resp = client.get("/api/clientes")
    assert clientes_resp.status_code == 200
    cliente_id = clientes_resp.json()[0]["id"]

    response = client.post(
        "/api/pedidos",
        json={
            "cliente_id": cliente_id,
            "detalles": [{"producto_id": 999999, "cantidad": 1}],
        },
    )
    assert response.status_code == 404
    assert "Producto 999999 no encontrado" in response.json()["detail"]


def test_crear_pedido_sin_detalles():
    clientes_resp = client.get("/api/clientes")
    assert clientes_resp.status_code == 200
    cliente_id = clientes_resp.json()[0]["id"]

    response = client.post(
        "/api/pedidos",
        json={
            "cliente_id": cliente_id,
            "detalles": [],
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "El pedido debe contener al menos un producto"


def test_crear_pedido_stock_insuficiente():
    # Crear producto con stock bajo
    payload = {
        "nombre": "Pan Escaso",
        "descripcion": "Prueba stock",
        "precio": 100,
        "stock": 1,
    }
    prod_resp = client.post("/api/productos", json=payload)
    assert prod_resp.status_code == 201
    producto_id = prod_resp.json()["id"]

    clientes_resp = client.get("/api/clientes")
    assert clientes_resp.status_code == 200
    cliente_id = clientes_resp.json()[0]["id"]

    # Intentar pedir más que el stock disponible
    response = client.post(
        "/api/pedidos",
        json={
            "cliente_id": cliente_id,
            "detalles": [{"producto_id": producto_id, "cantidad": 2}],
        },
    )
    assert response.status_code == 400
    assert f"Stock insuficiente para el producto {producto_id}" in response.json()["detail"]
