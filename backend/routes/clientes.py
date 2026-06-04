from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, constr

from database import get_connection

router = APIRouter()


class ClienteCreate(BaseModel):
    nombre: constr(min_length=1)
    telefono: Optional[constr(min_length=7)] = None
    correo: Optional[EmailStr] = None


class ClienteUpdate(BaseModel):
    nombre: Optional[constr(min_length=1)] = None
    telefono: Optional[constr(min_length=7)] = None
    correo: Optional[EmailStr] = None


class Cliente(BaseModel):
    id: int
    nombre: str
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None


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


@router.put("/clientes/{cliente_id}", response_model=Cliente)
def actualizar_cliente(cliente_id: int, cliente_data: ClienteUpdate):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT id FROM clientes WHERE id = ?", (cliente_id,))
    if cursor.fetchone() is None:
        conexion.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )

    updates = []
    values = []

    if cliente_data.nombre is not None:
        updates.append("nombre = ?")
        values.append(cliente_data.nombre)
    if cliente_data.telefono is not None:
        updates.append("telefono = ?")
        values.append(cliente_data.telefono)
    if cliente_data.correo is not None:
        updates.append("correo = ?")
        values.append(cliente_data.correo)

    if updates:
        values.append(cliente_id)
        cursor.execute(
            f"UPDATE clientes SET {', '.join(updates)} WHERE id = ?",
            values
        )
        conexion.commit()

    cursor.execute(
        "SELECT id, nombre, telefono, correo FROM clientes WHERE id = ?",
        (cliente_id,)
    )
    cliente = cursor.fetchone()
    conexion.close()

    return {
        "id": cliente[0],
        "nombre": cliente[1],
        "telefono": cliente[2],
        "correo": cliente[3]
    }


@router.delete("/clientes/{cliente_id}")
def eliminar_cliente(cliente_id: int):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT id FROM clientes WHERE id = ?", (cliente_id,))
    if cursor.fetchone() is None:
        conexion.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado"
        )

    cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    conexion.commit()
    conexion.close()

    return {"mensaje": "Cliente eliminado correctamente"}