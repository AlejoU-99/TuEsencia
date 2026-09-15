import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse, unquote
import json
import re
import time


# ============================================================
# CONFIGURACIÓN
# ============================================================

BASE_URL = "https://muranosteel.com/tienda/"

TOTAL_PAGES = 42

DELAY_BETWEEN_REQUESTS = 1.0

REQUEST_TIMEOUT = 30


# ============================================================
# HEADERS
# ============================================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/152.0.0.0 Safari/537.36"
    ),

    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,image/avif,image/webp,"
        "image/apng,*/*;q=0.8"
    ),

    "Accept-Language": "es-CO,es;q=0.9,en;q=0.8",

    "Connection": "keep-alive",
}


# ============================================================
# RUTA DEL PROYECTO
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_FILE = PROJECT_ROOT / "catalogo.json"


# ============================================================
# SESIÓN HTTP
# ============================================================

session = requests.Session()

session.headers.update(
    HEADERS
)


# ============================================================
# DESCARGAR PÁGINA
# ============================================================

def descargar_pagina(url):

    print()
    print("-" * 70)
    print("DESCARGANDO")
    print(url)

    response = session.get(
        url,
        timeout=REQUEST_TIMEOUT
    )

    print(
        f"HTTP Status: {response.status_code}"
    )

    response.raise_for_status()

    return response.text


# ============================================================
# CONSTRUIR URL DE PÁGINA
# ============================================================

def construir_url_pagina(numero):

    if numero == 1:

        return BASE_URL

    return (
        f"{BASE_URL}"
        f"page/{numero}/"
    )


# ============================================================
# OBTENER SLUG
# ============================================================

def obtener_slug(url):

    if not url:
        return None

    try:

        parsed = urlparse(url)

        path = parsed.path.rstrip("/")

        slug = path.split("/")[-1]

        return unquote(slug)

    except Exception:

        return None


# ============================================================
# OBTENER SKU
# ============================================================

def obtener_sku(texto):

    if not texto:
        return None

    resultado = re.search(
        r"\bSKU[-_\s]?(\d+)\b",
        texto,
        re.IGNORECASE
    )

    if resultado:

        return (
            f"SKU{resultado.group(1)}"
        )

    return None


# ============================================================
# OBTENER URL DEL PRODUCTO
# ============================================================

def obtener_url_producto(producto):

    enlace = producto.select_one(
        "a[href*='/producto/']"
    )

    if enlace:

        return enlace.get(
            "href"
        )

    return None


# ============================================================
# OBTENER IMÁGENES
# ============================================================

def obtener_imagenes(producto):

    imagen_elemento = producto.select_one(
        "img"
    )

    if not imagen_elemento:

        return None, None

    imagen = (
        imagen_elemento.get("src")
        or imagen_elemento.get("data-src")
    )

    srcset = (
        imagen_elemento.get("srcset")
        or imagen_elemento.get("data-srcset")
    )

    imagen_alta = imagen

    if srcset:

        opciones = []

        for item in srcset.split(","):

            partes = item.strip().split()

            if not partes:
                continue

            url = partes[0]

            ancho = 0

            if len(partes) > 1:

                match = re.search(
                    r"(\d+)w",
                    partes[1]
                )

                if match:

                    ancho = int(
                        match.group(1)
                    )

            opciones.append(
                {
                    "url": url,
                    "ancho": ancho
                }
            )

        if opciones:

            opciones.sort(
                key=lambda x: x["ancho"]
            )

            imagen_alta = opciones[-1]["url"]

    return imagen, imagen_alta


# ============================================================
# OBTENER CATEGORÍA
# ============================================================

def obtener_categoria(producto):

    clases = producto.get(
        "class",
        []
    )

    for clase in clases:

        if clase.startswith(
            "product_cat-"
        ):

            return clase.replace(
                "product_cat-",
                "",
                1
            )

    return None


# ============================================================
# OBTENER NOMBRE
# ============================================================

def obtener_nombre(
    producto,
    slug,
    imagen_elemento
):

    # --------------------------------------------------------
    # 1. Título WooCommerce
    # --------------------------------------------------------

    selectores = [
        ".woocommerce-loop-product__title",
        ".product-title",
        ".woocommerce-loop-product__title a"
    ]

    for selector in selectores:

        elemento = producto.select_one(
            selector
        )

        if elemento:

            texto = elemento.get_text(
                " ",
                strip=True
            )

            if texto:

                return texto

    # --------------------------------------------------------
    # 2. ALT DE IMAGEN
    # --------------------------------------------------------

    if imagen_elemento:

        alt = imagen_elemento.get(
            "alt"
        )

        if alt:

            alt = alt.strip()

            if alt:

                return alt

    # --------------------------------------------------------
    # 3. SLUG
    # --------------------------------------------------------

    return slug


# ============================================================
# LIMPIAR PRECIO
# ============================================================

def limpiar_precio(texto):

    if not texto:
        return None

    # Buscar solamente el primer número
    resultado = re.search(
        r"\d[\d.,]*",
        texto
    )

    if not resultado:

        return None

    numero = resultado.group(
        0
    )

    # El catálogo utiliza separadores
    # de miles.

    numero = re.sub(
        r"[.,]",
        "",
        numero
    )

    try:

        return int(numero)

    except ValueError:

        return None


# ============================================================
# EXTRAER PRECIOS CORRECTAMENTE
# ============================================================

def extraer_precios(producto):

    precio_elemento = producto.select_one(
        ".price"
    )

    if not precio_elemento:

        return {
            "precio": None,
            "precio_anterior": None,
            "en_descuento": False
        }

    # ========================================================
    # PRODUCTO CON DESCUENTO
    # ========================================================

    precio_original_elemento = (
        precio_elemento.select_one("del")
    )

    precio_actual_elemento = (
        precio_elemento.select_one("ins")
    )

    if (
        precio_original_elemento
        and precio_actual_elemento
    ):

        precio_original_texto = (
            precio_original_elemento.get_text(
                " ",
                strip=True
            )
        )

        precio_actual_texto = (
            precio_actual_elemento.get_text(
                " ",
                strip=True
            )
        )

        precio_original = limpiar_precio(
            precio_original_texto
        )

        precio_actual = limpiar_precio(
            precio_actual_texto
        )

        return {
            "precio": precio_actual,
            "precio_anterior": precio_original,
            "en_descuento": True
        }

    # ========================================================
    # PRODUCTO SIN DESCUENTO
    # ========================================================

    # No utilizamos get_text() del bloque completo
    # si existen elementos internos que puedan contener
    # información adicional.

    precio_simple = (
        precio_elemento.select_one(
            "bdi"
        )
    )

    if precio_simple:

        precio_texto = (
            precio_simple.get_text(
                " ",
                strip=True
            )
        )

    else:

        precio_texto = (
            precio_elemento.get_text(
                " ",
                strip=True
            )
        )

    precio = limpiar_precio(
        precio_texto
    )

    return {
        "precio": precio,
        "precio_anterior": None,
        "en_descuento": False
    }


# ============================================================
# EXTRAER PRODUCTO
# ============================================================

def extraer_producto(producto):

    # --------------------------------------------------------
    # URL
    # --------------------------------------------------------

    url_producto = (
        obtener_url_producto(
            producto
        )
    )

    # --------------------------------------------------------
    # SLUG
    # --------------------------------------------------------

    slug = obtener_slug(
        url_producto
    )

    # --------------------------------------------------------
    # IMAGEN
    # --------------------------------------------------------

    imagen_elemento = (
        producto.select_one("img")
    )

    imagen, imagen_alta = (
        obtener_imagenes(
            producto
        )
    )

    # --------------------------------------------------------
    # NOMBRE
    # --------------------------------------------------------

    nombre = obtener_nombre(
        producto,
        slug,
        imagen_elemento
    )

    # --------------------------------------------------------
    # SKU
    # --------------------------------------------------------

    sku = obtener_sku(
        f"{nombre or ''} {slug or ''}"
    )

    # --------------------------------------------------------
    # CATEGORÍA
    # --------------------------------------------------------

    categoria = obtener_categoria(
        producto
    )

    # --------------------------------------------------------
    # FALLBACK CATEGORÍA
    # --------------------------------------------------------

    if not categoria and slug:

        partes = slug.split("-")

        if partes:

            categoria = partes[0]

    # --------------------------------------------------------
    # PRECIOS
    # --------------------------------------------------------

    precios = extraer_precios(
        producto
    )

    # --------------------------------------------------------
    # PRODUCTO FINAL
    # --------------------------------------------------------

    return {
        "nombre": nombre,

        "slug": slug,

        "sku": sku,

        "precio": precios["precio"],

        "precio_anterior": (
            precios["precio_anterior"]
        ),

        "en_descuento": (
            precios["en_descuento"]
        ),

        "moneda": "COP",

        "categoria": categoria,

        "url": url_producto,

        "imagen": imagen,

        "imagen_alta": imagen_alta
    }


# ============================================================
# EXTRAER PRODUCTOS DE UNA PÁGINA
# ============================================================

def extraer_productos(html):

    soup = BeautifulSoup(
        html,
        "lxml"
    )

    elementos = soup.select(
        "li.product"
    )

    productos = []

    for elemento in elementos:

        try:

            producto = extraer_producto(
                elemento
            )

            if producto["url"]:

                productos.append(
                    producto
                )

        except Exception as error:

            print(
                "ERROR procesando producto:",
                error
            )

    return productos


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("MURANO STEEL - SCRAPER V3.1")
    print("=" * 70)

    todos_los_productos = []

    errores = []

    # ========================================================
    # RECORRER 42 PÁGINAS
    # ========================================================

    for pagina in range(
        1,
        TOTAL_PAGES + 1
    ):

        url = construir_url_pagina(
            pagina
        )

        try:

            html = descargar_pagina(
                url
            )

            productos = extraer_productos(
                html
            )

            print(
                f"Productos encontrados: "
                f"{len(productos)}"
            )

            todos_los_productos.extend(
                productos
            )

        except Exception as error:

            print()
            print(
                f"ERROR EN PÁGINA {pagina}"
            )

            print(error)

            errores.append(
                {
                    "pagina": pagina,
                    "error": str(error)
                }
            )

        if pagina < TOTAL_PAGES:

            time.sleep(
                DELAY_BETWEEN_REQUESTS
            )

    # ========================================================
    # ELIMINAR DUPLICADOS
    # ========================================================

    productos_unicos = []

    urls_vistas = set()

    duplicados = 0

    for producto in todos_los_productos:

        url = producto.get(
            "url"
        )

        if not url:
            continue

        if url in urls_vistas:

            duplicados += 1

            continue

        urls_vistas.add(
            url
        )

        productos_unicos.append(
            producto
        )

    # ========================================================
    # ESTADÍSTICAS
    # ========================================================

    sin_nombre = sum(
        1
        for p in productos_unicos
        if not p.get("nombre")
    )

    sin_sku = sum(
        1
        for p in productos_unicos
        if not p.get("sku")
    )

    sin_precio = sum(
        1
        for p in productos_unicos
        if p.get("precio") is None
    )

    sin_imagen = sum(
        1
        for p in productos_unicos
        if not p.get("imagen")
    )

    sin_categoria = sum(
        1
        for p in productos_unicos
        if not p.get("categoria")
    )

    productos_descuento = sum(
        1
        for p in productos_unicos
        if p.get("en_descuento")
    )

    # ========================================================
    # GUARDAR JSON
    # ========================================================

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            productos_unicos,
            archivo,
            ensure_ascii=False,
            indent=2
        )

    # ========================================================
    # MUESTRA
    # ========================================================

    print()
    print("=" * 70)
    print("MUESTRA DE PRODUCTOS")
    print("=" * 70)

    for numero, producto in enumerate(
        productos_unicos[:10],
        start=1
    ):

        print()
        print(
            f"{numero}. "
            f"{producto['nombre']}"
        )

        print(
            f"   SKU: "
            f"{producto['sku']}"
        )

        print(
            f"   Categoría: "
            f"{producto['categoria']}"
        )

        print(
            f"   Precio actual: "
            f"{producto['precio']}"
        )

        print(
            f"   Precio anterior: "
            f"{producto['precio_anterior']}"
        )

        print(
            f"   En descuento: "
            f"{producto['en_descuento']}"
        )

        print(
            f"   Imagen HD: "
            f"{producto['imagen_alta']}"
        )

    # ========================================================
    # RESUMEN FINAL
    # ========================================================

    print()
    print("=" * 70)
    print("RESUMEN FINAL")
    print("=" * 70)

    print(
        f"Páginas procesadas: "
        f"{TOTAL_PAGES}"
    )

    print(
        f"Productos encontrados: "
        f"{len(todos_los_productos)}"
    )

    print(
        f"Productos únicos: "
        f"{len(productos_unicos)}"
    )

    print(
        f"Duplicados eliminados: "
        f"{duplicados}"
    )

    print(
        f"Sin nombre: "
        f"{sin_nombre}"
    )

    print(
        f"Sin SKU: "
        f"{sin_sku}"
    )

    print(
        f"Sin precio: "
        f"{sin_precio}"
    )

    print(
        f"Sin categoría: "
        f"{sin_categoria}"
    )

    print(
        f"Sin imagen: "
        f"{sin_imagen}"
    )

    print(
        f"Productos con descuento: "
        f"{productos_descuento}"
    )

    print(
        f"Errores de página: "
        f"{len(errores)}"
    )

    # ========================================================
    # ERRORES
    # ========================================================

    if errores:

        print()
        print("DETALLE DE ERRORES")

        for error in errores:

            print(
                f"Página {error['pagina']}: "
                f"{error['error']}"
            )

    # ========================================================
    # UBICACIÓN JSON
    # ========================================================

    print()
    print(
        "JSON generado:"
    )

    print(
        OUTPUT_FILE
    )

    print()
    print("=" * 70)
    print("SCRAPER V3.1 FINALIZADO")
    print("=" * 70)


# ============================================================
# EJECUTAR
# ============================================================

if __name__ == "__main__":

    main()