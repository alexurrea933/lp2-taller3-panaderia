from fastapi import FastAPI

from routes.productos import router as productos_router
from routes.clientes import router as clientes_router
from routes.pedidos import router as pedidos_router

app = FastAPI(
    title="Panadería Delicia API"
)

@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a la API de la Panadería"
    }

app.include_router(productos_router)
app.include_router(clientes_router)
app.include_router(pedidos_router)