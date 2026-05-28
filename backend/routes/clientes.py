from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from backend.database import get_connection

router = APIRouter()


class ClienteCreate(BaseModel):
    nombre: str
    telefono: Optional[str] = None
    correo: Optional[str] = None


class Cliente(BaseModel):
    id: int
    nombre: str
    telefono: Optional[str] = None
    correo: Optional[str] = None


@router.get("/clientes", response_model=List[Cliente])
def obtener_clientes():
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT id, nombre, telefono, correo FROM clientes")
    clientes = cursor.fetchall()

    conexion.close()

    resultado = []
    for cliente in clientes:
        resultado.append({
            "id": cliente[0],
            "nombre": cliente[1],
            "telefono": cliente[2],
            "correo": cliente[3],
        })

    return resultado


@router.get("/clientes/{cliente_id}", response_model=Cliente)
def obtener_cliente(cliente_id: int):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT id, nombre, telefono, correo FROM clientes WHERE id = ?",
        (cliente_id,),
    )
    cliente = cursor.fetchone()
    conexion.close()

    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado",
        )

    return {
        "id": cliente[0],
        "nombre": cliente[1],
        "telefono": cliente[2],
        "correo": cliente[3],
    }


@router.post("/clientes", response_model=Cliente, status_code=status.HTTP_201_CREATED)
def crear_cliente(cliente: ClienteCreate):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO clientes (nombre, telefono, correo) VALUES (?, ?, ?)",
        (cliente.nombre, cliente.telefono, cliente.correo),
    )
    cliente_id = cursor.lastrowid
    conexion.commit()
    conexion.close()

    return {
        "id": cliente_id,
        "nombre": cliente.nombre,
        "telefono": cliente.telefono,
        "correo": cliente.correo,
    }
