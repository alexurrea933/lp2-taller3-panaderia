from fastapi import APIRouter
from database import get_connection

router = APIRouter()

@router.get("/pedidos")
def obtener_pedidos():

    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM pedidos")
    pedidos = cursor.fetchall()

    conexion.close()

    resultado = []

    for pedido in pedidos:
        resultado.append({
            "id": pedido[0],
            "cliente_id": pedido[1],
            "fecha": pedido[2],
            "total": pedido[3]
        })

    return resultado