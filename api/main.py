from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.productos import router as productos_router


app = FastAPI(
    title="TuEsencia API",
    description="API del catálogo de productos",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(productos_router)


@app.get("/")
def inicio():
    return {
        "mensaje": "TuEsencia API funcionando",
        "version": "1.0.0"
    }