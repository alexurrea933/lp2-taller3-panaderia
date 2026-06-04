import sys
import os

# Agregar el directorio backend al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_obtener_clientes():
    response = client.get("/api/clientes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert all("nombre" in cliente for cliente in response.json())


def test_crear_actualizar_eliminar_cliente():
    payload = {
        "nombre": "Cliente Prueba",
        "telefono": "3001231234",
        "correo": "prueba@mail.com",
    }
    response = client.post("/api/clientes", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == payload["nombre"]
    assert data["telefono"] == payload["telefono"]
    assert data["correo"] == payload["correo"]
    cliente_id = data["id"]

    update_payload = {
        "nombre": "Cliente Actualizado",
        "telefono": "3009999999",
    }
    update_response = client.put(f"/api/clientes/{cliente_id}", json=update_payload)
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["nombre"] == update_payload["nombre"]
    assert updated["telefono"] == update_payload["telefono"]

    delete_response = client.delete(f"/api/clientes/{cliente_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["mensaje"] == "Cliente eliminado correctamente"

    no_existe_resp = client.get(f"/api/clientes/{cliente_id}")
    assert no_existe_resp.status_code == 404


def test_obtener_cliente_por_id():
    clientes_resp = client.get("/api/clientes")
    assert clientes_resp.status_code == 200
    clientes = clientes_resp.json()
    assert len(clientes) > 0

    cliente_id = clientes[0]["id"]
    response = client.get(f"/api/clientes/{cliente_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == cliente_id
    assert "nombre" in data
