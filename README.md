# Panaderia Delicia — Proyecto

Este repositorio contiene el backend (FastAPI) y un frontend estático.

Estructura principal:
- `backend/`: API en Python (FastAPI). Ver [backend/README.md](backend/README.md) para setup y tests.
- `frontend/`: ejemplo simple de frontend (HTML/JS/CSS). Ver `frontend/README.md`.

Resumen rápido para desarrolladores:
- Para trabajar con el backend, sigue las instrucciones en `backend/README.md`.
- Para el frontend, abre `frontend/index.html` en un navegador o sirve la carpeta estática.

CI:
- Hay un workflow de GitHub Actions en `.github/workflows/ci.yml` que ejecuta los tests del backend.

Ejemplos de endpoints
---------------------

Productos
- `GET /api/productos` — lista todos los productos.
- `GET /api/productos/{id}` — obtiene producto por id.
- `POST /api/productos` — crear producto. Payload JSON de ejemplo:

```json
{
   "nombre": "Pan Cacho",
   "descripcion": "Pan fresco",
   "precio": 500,
   "stock": 100
}
```
- `PUT /api/productos/{id}` — actualizar producto (envía solo campos a modificar).
- `DELETE /api/productos/{id}` — eliminar producto.

Clientes
- `GET /api/clientes` — lista clientes.
- `GET /api/clientes/{id}` — obtiene cliente por id.
- `POST /api/clientes` — crear cliente. Payload JSON de ejemplo:

```json
{
   "nombre": "Cliente Prueba",
   "telefono": "3001231234",
   "correo": "cliente@mail.com"
}
```

Pedidos
- `GET /api/pedidos` — lista pedidos con sus detalles.
- `POST /api/pedidos` — crear pedido. Payload JSON de ejemplo:

```json
{
   "cliente_id": 1,
   "detalles": [{"producto_id": 2, "cantidad": 1}]
}
```

Ejemplos curl y respuestas
--------------------------

Crear producto (curl):

```bash
curl -s -X POST http://localhost:8000/api/productos \
   -H "Content-Type: application/json" \
   -d '{"nombre":"Pan Cacho","descripcion":"Pan fresco","precio":500,"stock":100}'
```

Respuesta exitosa (201):

```json
{
   "id": 10,
   "nombre": "Pan Cacho",
   "descripcion": "Pan fresco",
   "precio": 500.0,
   "stock": 100
}
```

Crear cliente (curl):

```bash
curl -s -X POST http://localhost:8000/api/clientes \
   -H "Content-Type: application/json" \
   -d '{"nombre":"Cliente Prueba","telefono":"3001231234","correo":"cliente@mail.com"}'
```

Respuesta exitosa (201):

```json
{
   "id": 5,
   "nombre": "Cliente Prueba",
   "telefono": "3001231234",
   "correo": "cliente@mail.com"
}
```

Crear pedido (curl):

```bash
curl -s -X POST http://localhost:8000/api/pedidos \
   -H "Content-Type: application/json" \
   -d '{"cliente_id":1,"detalles":[{"producto_id":2,"cantidad":1}]}'
```

Respuesta exitosa (201):

```json
{
   "id": 12,
   "cliente_id": 1,
   "fecha": "2026-06-02T12:00:00+00:00",
   "total": 500.0,
   "detalles": [{"producto_id": 2, "cantidad": 1, "subtotal": 500.0}]
}
```

Contribuir
---------

1. Haz fork del repositorio y crea una rama nueva: `git checkout -b feat/mi-cambio`.
2. Ejecuta tests localmente y asegúrate de que pasen antes de abrir PR.

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

3. Abre un PR contra `main` describiendo el cambio. El CI ejecutará los tests automáticamente.

Notas:
- Mantén los cambios mínimos y ejecuta `pytest` antes de push.
- Si añades nuevas dependencias, agrega las mismas a `backend/requirements.txt`.

# Proyecto Base: Frontend + Backend

Este repositorio sirve como plantilla para el desarrollo de un sitio web moderno con **frontend en Next.js + Tailwind CSS** y **backend en FastAPI + SQLite + pytest**. La estructura está diseñada para mantener una separación clara entre cliente y servidor, fomentar buenas prácticas y facilitar la escalabilidad.


## 📂 Estructura del proyecto

```
project-root/
│
├── frontend/                # Aplicación cliente con Next.js y Tailwind CSS
│   ├── SKILL.md             # Buenas prácticas para frontend
│   ├── package.json         # Dependencias y scripts de frontend
│   └── README.md            # Documentación específica del frontend
│
├── backend/                 # API con FastAPI, SQLite y pytest
│   ├── SKILL.md             # Buenas prácticas para backend
│   ├── requirements.txt     # Dependencias de Python
│   ├── pytest.ini           # Configuración de pytest
│   └── README.md            # Documentación específica del backend
│
├── docs/                    # Documentación general del proyecto
│   └── architecture.md      # Explicación de arquitectura y decisiones
│
├── .gitignore               # Ignorar archivos comunes
├── README.md                # Este archivo
└── LICENSE                  # Licencia del proyecto
```


## 🚀 Tecnologías principales

- **Next.js**: Framework de React para aplicaciones web modernas.
- **Tailwind CSS**: Librería de utilidades CSS para diseño rápido y consistente.
- **FastAPI**: Framework Python para construir APIs rápidas y tipadas.
- **SQLite**: Base de datos ligera y embebida.
- **pytest**: Framework de pruebas para Python.


## 📖 Documentación

- **frontend/SKILL.md**: Guía de buenas prácticas para desarrollo con Next.js y Tailwind.
- **backend/SKILL.md**: Guía de buenas prácticas para FastAPI, SQLite y pytest.
- **docs/architecture.md**: Explicación de la arquitectura, comunicación entre frontend y backend, y posibles mejoras futuras.


## 🛠️ Instalación inicial

Cada entorno se configura de manera independiente:

### Frontend
1. Entrar al directorio `frontend/`.
2. Instalar dependencias:  
   ```bash
   npm install
   ```
3. Levantar servidor de desarrollo:  
   ```bash
   npm run dev
   ```

### Backend
1. Desde la raíz del proyecto, activa el entorno virtual existente:
   ```bash
   source ./venv/bin/activate
   ```
2. Instala dependencias si aún no lo hiciste:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Levanta el servidor FastAPI desde la raíz del proyecto:
   ```bash
   uvicorn backend.main:app --reload
   ```

## 🚢 Despliegue del backend

### Opción 1: desplegar localmente con Uvicorn
1. Activa el entorno virtual desde la raíz del proyecto:
   ```bash
   source ./venv/bin/activate
   ```
2. Ejecuta el servidor en `0.0.0.0:8000` desde la raíz del proyecto:
   ```bash
   uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```
3. Abre la API en el navegador:
   ```
   http://localhost:8000
   ```

### Opción 2: desplegar con Docker
1. Construye la imagen desde la carpeta raíz:
   ```bash
   docker build -t panaderia-backend .
   ```
2. Inicia el contenedor:
   ```bash
   docker run -p 8000:8000 panaderia-backend
   ```
3. Si quieres usar `docker-compose`:
   ```bash
   docker compose up --build
   ```

## 📌 Próximos pasos

- Definir la primera ruta de prueba en el backend.
- Configurar Tailwind en el frontend.
- Documentar la comunicación entre cliente y servidor en `docs/architecture.md`.
- Implementar pruebas iniciales con pytest.

