from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, PositiveInt, conint

from database import get_connection

router = APIRouter()


class DetallePedidoCreate(BaseModel):
    producto_id: conint(gt=0)
    cantidad: PositiveInt


class PedidoCreate(BaseModel):
    cliente_id: conint(gt=0)
    detalles: List[DetallePedidoCreate]
    fecha: Optional[str] = None


class PedidoDetalle(BaseModel):
    producto_id: int
    cantidad: int
    subtotal: float


class PedidoResponse(BaseModel):
    id: int
    cliente_id: int
    fecha: str
    total: float
    detalles: List[PedidoDetalle]


@router.get("/pedidos", response_model=List[PedidoResponse])
def obtener_pedidos():
    conexion = get_connection()
    cursor = conexion.cursor()

    cursor.execute("SELECT id, cliente_id, fecha, total FROM pedidos")
    pedidos = cursor.fetchall()

    resultado = []
    for pedido in pedidos:
        pedido_id = pedido[0]
        cursor.execute(
            "SELECT producto_id, cantidad, subtotal FROM detalle_pedido WHERE pedido_id = ?",
            (pedido_id,),
        )
        detalles_db = cursor.fetchall()
        detalles = [
            {
                "producto_id": detalle[0],
                "cantidad": detalle[1],
                "subtotal": detalle[2],
            }
            for detalle in detalles_db
        ]
        resultado.append(
            {
                "id": pedido_id,
                "cliente_id": pedido[1],
                "fecha": pedido[2],
                "total": pedido[3],
                "detalles": detalles,
            }
        )

    conexion.close()
    return resultado


@router.post("/pedidos", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def crear_pedido(pedido: PedidoCreate):
    if not pedido.detalles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El pedido debe contener al menos un producto",
        )
    conexion = get_connection()
    cursor = conexion.cursor()

    try:
        cursor.execute("SELECT id FROM clientes WHERE id = ?", (pedido.cliente_id,))
        cliente = cursor.fetchone()
        if cliente is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado",
            )

        fecha_registro = pedido.fecha or datetime.now(timezone.utc).isoformat()
        total = 0.0
        detalles_registro = []

        for item in pedido.detalles:
            cursor.execute(
                "SELECT precio, stock FROM productos WHERE id = ?",
                (item.producto_id,),
            )
            producto = cursor.fetchone()
            if producto is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Producto {item.producto_id} no encontrado",
                )

            precio, stock = producto
            if item.cantidad > stock:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Stock insuficiente para el producto {item.producto_id}",
                )

            subtotal = precio * item.cantidad
            total += subtotal
            detalles_registro.append(
                {
                    "producto_id": item.producto_id,
                    "cantidad": item.cantidad,
                    "subtotal": subtotal,
                }
            )

        cursor.execute(
            "INSERT INTO pedidos (cliente_id, fecha, total) VALUES (?, ?, ?)",
            (pedido.cliente_id, fecha_registro, total),
        )
        pedido_id = cursor.lastrowid

        for detalle in detalles_registro:
            cursor.execute(
                "INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, subtotal) VALUES (?, ?, ?, ?)",
                (pedido_id, detalle["producto_id"], detalle["cantidad"], detalle["subtotal"]),
            )
            cursor.execute(
                "UPDATE productos SET stock = stock - ? WHERE id = ?",
                (detalle["cantidad"], detalle["producto_id"]),
            )

        conexion.commit()

    except HTTPException:
        conexion.rollback()
        conexion.close()
        raise
    except Exception:
        conexion.rollback()
        conexion.close()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al crear el pedido",
        )
    finally:
        try:
            conexion.close()
        except Exception:
            pass

    return {
        "id": pedido_id,
        "cliente_id": pedido.cliente_id,
        "fecha": fecha_registro,
        "total": total,
        "detalles": detalles_registro,
    }
