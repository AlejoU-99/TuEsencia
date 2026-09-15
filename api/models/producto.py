from pydantic import BaseModel
from typing import Optional


class AtributosProducto(BaseModel):
    tipo: Optional[str] = None
    color: Optional[str] = None
    estilo: Optional[str] = None
    material: Optional[str] = None


class Producto(BaseModel):
    id: int
    nombre: str
    slug: str
    sku: str

    precio_venta: int
    precio_anterior: Optional[int] = None
    en_descuento: bool

    moneda: str
    categoria: str

    url: str
    imagen: str
    imagen_alta: str

    atributos: AtributosProducto


class RespuestaProductos(BaseModel):
    productos: list[Producto]
    total: int
    pagina: int
    limite: int
    total_paginas: int