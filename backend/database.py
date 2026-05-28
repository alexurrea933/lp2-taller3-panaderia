import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "panaderia.db"

SCHEMA = [
    """
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL
)
""",
    """
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT,
    correo TEXT
)
""",
    """
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    fecha TEXT,
    total REAL,
    FOREIGN KEY(cliente_id) REFERENCES clientes(id)
)
""",
    """
CREATE TABLE IF NOT EXISTS detalle_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER,
    producto_id INTEGER,
    cantidad INTEGER,
    subtotal REAL,
    FOREIGN KEY(pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY(producto_id) REFERENCES productos(id)
)
"""
]

SEED_PRODUCTS = [
    ("Pan Cacho", "Pan CREMA", 500, 1000),
    ("Pan agridulce", "Pan Mantequilla", 600, 2000),
    ("Torta de chocolate", "Porción individual", 2000, 2000),
]

SEED_CLIENTES = [
    ("Juan Pérez", "3001234567", "juan@gmail.com"),
    ("María López", "3017654321", "maria@gmail.com"),
]


def get_connection():
    conexion = sqlite3.connect(DB_PATH)
    return conexion


def init_db():
    conexion = get_connection()
    cursor = conexion.cursor()

    for statement in SCHEMA:
        cursor.execute(statement)

    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO productos (nombre, descripcion, precio, stock) VALUES (?, ?, ?, ?)",
            SEED_PRODUCTS,
        )

    cursor.execute("SELECT COUNT(*) FROM clientes")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO clientes (nombre, telefono, correo) VALUES (?, ?, ?)",
            SEED_CLIENTES,
        )

    conexion.commit()
    conexion.close()


init_db()
