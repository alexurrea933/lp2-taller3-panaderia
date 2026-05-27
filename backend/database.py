import sqlite3

conexion = sqlite3.connect("panaderia.db")
cursor = conexion.cursor()

# tabla productos
cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL
)
""")

# tabla clientes
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT,
    correo TEXT
)
""")

# tabla pedidos
cursor.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    fecha TEXT,
    total REAL,
    FOREIGN KEY(cliente_id) REFERENCES clientes(id)
)
""")

# detalle pedido
cursor.execute("""
CREATE TABLE IF NOT EXISTS detalle_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER,
    producto_id INTEGER,
    cantidad INTEGER,
    subtotal REAL,
    FOREIGN KEY(pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY(producto_id) REFERENCES productos(id)
)
""")

cursor.execute("""
INSERT INTO productos (nombre, descripcion, precio, stock)
VALUES
('Pan Cacho', 'Pan CREMA', 500, 1000),
('Pan agridulce', 'Pan Mantequilla', 600, 2000),
('Torta de chocolate', 'Porción individual', 2000, 2000)
""")

cursor.execute("""
INSERT INTO clientes (nombre, telefono, correo)
VALUES
('Juan Pérez', '3001234567', 'juan@gmail.com'),
('María López', '3017654321', 'maria@gmail.com')
""")

conexion.commit()
conexion.close()

print("Base de datos y tablas creadas correctamente")