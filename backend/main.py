from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.productos import router as productos_router
from routes.clientes import router as clientes_router
from routes.pedidos import router as pedidos_router

app = FastAPI(
    title="Panaderia Delicia API",
    description="API para gestion de panaderia",
    version="1.0.0"
)

# Configurar CORS para el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a la API de la Panaderia",
        "version": "1.0.0"
    }

app.include_router(productos_router, prefix="/api", tags=["Productos"])
app.include_router(clientes_router, prefix="/api", tags=["Clientes"])
app.include_router(pedidos_router, prefix="/api", tags=["Pedidos"])