from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_productos():
    response = client.get("/productos")

    assert response.status_code == 200