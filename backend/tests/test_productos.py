import sys
import os

# Agregar el directorio backend al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_obtener_productos():
    response = client.get("/api/productos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_crear_actualizar_eliminar_producto():
    payload = {
        "nombre": "Pan de Prueba",
        "descripcion": "Pan para testing",
        "precio": 1500,
        "stock": 50,
    }
    response = client.post("/api/productos", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == payload["nombre"]
    assert data["descripcion"] == payload["descripcion"]
    assert data["precio"] == payload["precio"]
    assert data["stock"] == payload["stock"]
    producto_id = data["id"]

    update_payload = {
        "nombre": "Pan Update",
        "precio": 1600,
    }
    update_response = client.put(f"/api/productos/{producto_id}", json=update_payload)
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["nombre"] == update_payload["nombre"]
    assert updated["precio"] == update_payload["precio"]

    delete_response = client.delete(f"/api/productos/{producto_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["mensaje"] == "Producto eliminado correctamente"

    no_existe_resp = client.get(f"/api/productos/{producto_id}")
    assert no_existe_resp.status_code == 404
