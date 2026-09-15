from collections import Counter
from math import ceil
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from api.models.producto import RespuestaProductos
from api.services.catalogo import cargar_catalogo


router = APIRouter(
    prefix="/api/productos",
    tags=["Productos"]
)


# ============================================================
# CONFIGURACIÓN
# ============================================================

FACETAS = [
    "categoria",
    "tipo",
    "color",
    "estilo",
    "material"
]


# ============================================================
# VALOR DE UN ATRIBUTO
# ============================================================

def obtener_valor_faceta(producto, faceta):

    if faceta == "categoria":
        return producto.get("categoria")

    atributos = producto.get("atributos") or {}

    return atributos.get(faceta)


# ============================================================
# COMPROBAR SI UN PRODUCTO CUMPLE LOS FILTROS
# ============================================================

def producto_coincide(
    producto,
    busqueda=None,
    categoria=None,
    tipo=None,
    color=None,
    estilo=None,
    material=None,
    precio_min=None,
    precio_max=None,
    excluir_faceta=None
):

    # --------------------------------------------------------
    # BÚSQUEDA
    # --------------------------------------------------------

    if busqueda:

        texto = busqueda.strip().lower()

        campos_busqueda = [
            str(producto.get("nombre", "")),
            str(producto.get("slug", "")),
            str(producto.get("sku", ""))
        ]

        if not any(
            texto in campo.lower()
            for campo in campos_busqueda
        ):
            return False


    # --------------------------------------------------------
    # CATEGORÍA
    # --------------------------------------------------------

    if (
        excluir_faceta != "categoria"
        and categoria
        and producto.get("categoria") != categoria
    ):
        return False


    # --------------------------------------------------------
    # ATRIBUTOS
    # --------------------------------------------------------

    atributos = producto.get("atributos") or {}


    if (
        excluir_faceta != "tipo"
        and tipo
        and atributos.get("tipo") != tipo
    ):
        return False


    if (
        excluir_faceta != "color"
        and color
        and atributos.get("color") != color
    ):
        return False


    if (
        excluir_faceta != "estilo"
        and estilo
        and atributos.get("estilo") != estilo
    ):
        return False


    if (
        excluir_faceta != "material"
        and material
        and atributos.get("material") != material
    ):
        return False


    # --------------------------------------------------------
    # PRECIO
    # --------------------------------------------------------

    precio = producto.get("precio_venta")


    if precio_min is not None:

        if precio is None or precio < precio_min:
            return False


    if precio_max is not None:

        if precio is None or precio > precio_max:
            return False


    return True


# ============================================================
# FILTRAR PRODUCTOS
# ============================================================

def filtrar_productos(
    productos,
    busqueda=None,
    categoria=None,
    tipo=None,
    color=None,
    estilo=None,
    material=None,
    precio_min=None,
    precio_max=None,
    excluir_faceta=None
):

    return [
        producto
        for producto in productos
        if producto_coincide(
            producto=producto,
            busqueda=busqueda,
            categoria=categoria,
            tipo=tipo,
            color=color,
            estilo=estilo,
            material=material,
            precio_min=precio_min,
            precio_max=precio_max,
            excluir_faceta=excluir_faceta
        )
    ]


# ============================================================
# ORDENAR PRODUCTOS
# ============================================================

def ordenar_productos(productos, orden):

    if orden == "precio_asc":

        return sorted(
            productos,
            key=lambda producto: producto.get(
                "precio_venta",
                0
            )
        )


    if orden == "precio_desc":

        return sorted(
            productos,
            key=lambda producto: producto.get(
                "precio_venta",
                0
            ),
            reverse=True
        )


    if orden == "nombre_asc":

        return sorted(
            productos,
            key=lambda producto: producto.get(
                "nombre",
                ""
            ).lower()
        )


    if orden == "nombre_desc":

        return sorted(
            productos,
            key=lambda producto: producto.get(
                "nombre",
                ""
            ).lower(),
            reverse=True
        )


    return productos


# ============================================================
# GET PRODUCTOS
# ============================================================

@router.get(
    "/",
    response_model=RespuestaProductos
)
def obtener_productos(
    pagina: int = Query(
        default=1,
        ge=1
    ),

    limite: int = Query(
        default=24,
        ge=1,
        le=100
    ),

    busqueda: Optional[str] = None,

    categoria: Optional[str] = None,

    tipo: Optional[str] = None,

    color: Optional[str] = None,

    estilo: Optional[str] = None,

    material: Optional[str] = None,

    precio_min: Optional[int] = Query(
        default=None,
        ge=0
    ),

    precio_max: Optional[int] = Query(
        default=None,
        ge=0
    ),

    orden: str = "default"
):

    productos = cargar_catalogo()


    # --------------------------------------------------------
    # FILTRADO
    # --------------------------------------------------------

    productos_filtrados = filtrar_productos(
        productos=productos,
        busqueda=busqueda,
        categoria=categoria,
        tipo=tipo,
        color=color,
        estilo=estilo,
        material=material,
        precio_min=precio_min,
        precio_max=precio_max
    )


    # --------------------------------------------------------
    # ORDEN
    # --------------------------------------------------------

    productos_filtrados = ordenar_productos(
        productos_filtrados,
        orden
    )


    # --------------------------------------------------------
    # PAGINACIÓN
    # --------------------------------------------------------

    total = len(productos_filtrados)

    total_paginas = max(
        1,
        ceil(total / limite)
    )


    inicio = (pagina - 1) * limite

    fin = inicio + limite

    productos_pagina = productos_filtrados[
        inicio:fin
    ]


    return {
        "productos": productos_pagina,
        "total": total,
        "pagina": pagina,
        "limite": limite,
        "total_paginas": total_paginas
    }


# ============================================================
# OPCIONES DINÁMICAS DE FILTROS
# ============================================================

@router.get(
    "/opciones"
)
def obtener_opciones_filtros(
    busqueda: Optional[str] = None,

    categoria: Optional[str] = None,

    tipo: Optional[str] = None,

    color: Optional[str] = None,

    estilo: Optional[str] = None,

    material: Optional[str] = None,

    precio_min: Optional[int] = Query(
        default=None,
        ge=0
    ),

    precio_max: Optional[int] = Query(
        default=None,
        ge=0
    )
):

    productos = cargar_catalogo()


    filtros = {
        "busqueda": busqueda,
        "categoria": categoria,
        "tipo": tipo,
        "color": color,
        "estilo": estilo,
        "material": material,
        "precio_min": precio_min,
        "precio_max": precio_max
    }


    respuesta = {}


    # --------------------------------------------------------
    # CALCULAR CADA FACETA
    #
    # Cada faceta ignora su propio filtro.
    # Los demás filtros sí se mantienen.
    # --------------------------------------------------------

    for faceta in FACETAS:

        productos_faceta = filtrar_productos(
            productos=productos,

            busqueda=filtros["busqueda"],

            categoria=filtros["categoria"],

            tipo=filtros["tipo"],

            color=filtros["color"],

            estilo=filtros["estilo"],

            material=filtros["material"],

            precio_min=filtros["precio_min"],

            precio_max=filtros["precio_max"],

            excluir_faceta=faceta
        )


        valores = Counter()


        for producto in productos_faceta:

            valor = obtener_valor_faceta(
                producto,
                faceta
            )

            if valor:

                valores[str(valor)] += 1


        opciones = []


        for valor, total in valores.most_common():

            opciones.append({
                "valor": valor,
                "total": total
            })


        # ----------------------------------------------------
        # Mantener visible el valor seleccionado si por
        # alguna combinación extrema quedara fuera.
        # ----------------------------------------------------

        valor_seleccionado = filtros.get(faceta)


        if (
            valor_seleccionado
            and not any(
                opcion["valor"] == valor_seleccionado
                for opcion in opciones
            )
        ):

            opciones.insert(
                0,
                {
                    "valor": valor_seleccionado,
                    "total": 0
                }
            )


        respuesta[faceta] = opciones


    return respuesta


# ============================================================
# CATEGORÍAS
# ============================================================

@router.get(
    "/categorias"
)
def obtener_categorias():

    productos = cargar_catalogo()

    contador = Counter(
        producto.get("categoria")
        for producto in productos
        if producto.get("categoria")
    )

    return {
        "categorias": [
            {
                "nombre": nombre,
                "total": total
            }
            for nombre, total
            in contador.most_common()
        ]
    }


# ============================================================
# ATRIBUTOS
# ============================================================

@router.get(
    "/atributos"
)
def obtener_atributos():

    productos = cargar_catalogo()


    respuesta = {}


    for atributo in [
        "tipo",
        "color",
        "estilo",
        "material"
    ]:

        contador = Counter()


        for producto in productos:

            atributos = producto.get(
                "atributos"
            ) or {}

            valor = atributos.get(
                atributo
            )

            if valor:

                contador[valor] += 1


        respuesta[atributo] = [
            {
                "valor": valor,
                "total": total
            }
            for valor, total
            in contador.most_common()
        ]


    return respuesta


# ============================================================
# PRODUCTO POR ID
# ============================================================

@router.get(
    "/{producto_id}"
)
def obtener_producto_por_id(
    producto_id: int
):

    productos = cargar_catalogo()


    for producto in productos:

        if producto.get("id") == producto_id:

            return producto


    raise HTTPException(
        status_code=404,
        detail="Producto no encontrado"
    )