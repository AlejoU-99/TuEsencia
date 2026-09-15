import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

CATALOGO_PATH = BASE_DIR / "catalogo.json"


def cargar_catalogo():
    with open(CATALOGO_PATH, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def obtener_productos():
    return cargar_catalogo()


def obtener_producto_por_id(producto_id: int):

    productos = cargar_catalogo()

    for producto in productos:

        if producto.get("id") == producto_id:
            return producto

    return None