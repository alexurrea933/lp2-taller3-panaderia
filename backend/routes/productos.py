from fastapi import APIRouter
from database import get_connection

router = APIRouter()

@router.get("/productos")
def obtener_productos():

    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    conexion.close()

    resultado = []

    for producto in productos:
        resultado.append({
            "id": producto[0],
            "nombre": producto[1],
            "descripcion": producto[2],
            "precio": producto[3],
            "stock": producto[4]
        })

    return resultado