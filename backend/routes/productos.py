from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, confloat, conint, constr

from database import get_connection

router = APIRouter()


class ProductoCreate(BaseModel):
    nombre: constr(min_length=1)
    descripcion: Optional[str] = None
    precio: confloat(gt=0)
    stock: conint(ge=0)


class ProductoUpdate(BaseModel):
    nombre: Optional[constr(min_length=1)] = None
    descripcion: Optional[str] = None
    precio: Optional[confloat(gt=0)] = None
    stock: Optional[conint(ge=0)] = None


class Producto(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    precio: float
    stock: int


@router.get("/productos", response_model=List[Producto])
def obtener_productos():
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT id, nombre, descripcion, precio, stock FROM productos")
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


@router.get("/productos/{producto_id}", response_model=Producto)
def obtener_producto(producto_id: int):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT id, nombre, descripcion, precio, stock FROM productos WHERE id = ?",
        (producto_id,)
    )
    producto = cursor.fetchone()
    conexion.close()

    if producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    return {
        "id": producto[0],
        "nombre": producto[1],
        "descripcion": producto[2],
        "precio": producto[3],
        "stock": producto[4]
    }


@router.post("/productos", response_model=Producto, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute(
        "INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (?, ?, ?, ?)",
        (producto.nombre, producto.descripcion, producto.precio, producto.stock)
    )
    producto_id = cursor.lastrowid
    conexion.commit()
    conexion.close()

    return {
        "id": producto_id,
        "nombre": producto.nombre,
        "descripcion": producto.descripcion,
        "precio": producto.precio,
        "stock": producto.stock
    }


@router.put("/productos/{producto_id}", response_model=Producto)
def actualizar_producto(producto_id: int, producto_data: ProductoUpdate):
    conexion = get_connection()
    cursor = conexion.cursor()

    # Verificar que existe
    cursor.execute("SELECT id FROM productos WHERE id = ?", (producto_id,))
    if cursor.fetchone() is None:
        conexion.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    # Construir query dinamico
    updates = []
    values = []
    
    if producto_data.nombre is not None:
        updates.append("nombre = ?")
        values.append(producto_data.nombre)
    if producto_data.descripcion is not None:
        updates.append("descripcion = ?")
        values.append(producto_data.descripcion)
    if producto_data.precio is not None:
        updates.append("precio = ?")
        values.append(producto_data.precio)
    if producto_data.stock is not None:
        updates.append("stock = ?")
        values.append(producto_data.stock)

    if updates:
        values.append(producto_id)
        cursor.execute(
            f"UPDATE productos SET {', '.join(updates)} WHERE id = ?",
            values
        )
        conexion.commit()

    # Obtener producto actualizado
    cursor.execute(
        "SELECT id, nombre, descripcion, precio, stock FROM productos WHERE id = ?",
        (producto_id,)
    )
    producto = cursor.fetchone()
    conexion.close()

    return {
        "id": producto[0],
        "nombre": producto[1],
        "descripcion": producto[2],
        "precio": producto[3],
        "stock": producto[4]
    }


@router.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int):
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT id FROM productos WHERE id = ?", (producto_id,))
    if cursor.fetchone() is None:
        conexion.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
    conexion.commit()
    conexion.close()

    return {"mensaje": "Producto eliminado correctamente"}