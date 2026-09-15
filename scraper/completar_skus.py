import json
import re
import time
import shutil
from pathlib import Path

import requests
from bs4 import BeautifulSoup


# ============================================================
# CONFIGURACIÓN
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = BASE_DIR / "catalogo.json"
BACKUP_PATH = BASE_DIR / "catalogo_backup_antes_skus.json"

DELAY_BETWEEN_REQUESTS = 1.0

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/140.0.0.0 Safari/537.36"
    )
}


# ============================================================
# FUNCIONES
# ============================================================

def extraer_sku(texto):
    """
    Busca formatos como:
    SKU12169
    SKU-12169
    SKU_12169
    sku12169
    """

    if not texto:
        return None

    match = re.search(
        r"\bSKU[-_\s]?(\d+)\b",
        texto,
        re.IGNORECASE
    )

    if match:
        return f"SKU{match.group(1)}"

    return None


def limpiar_nombre(nombre, sku):
    """
    Elimina el SKU pegado al final del nombre.
    """

    if not nombre:
        return nombre

    nombre = nombre.strip()

    if sku:
        patron = re.compile(
            rf"[-_\s]*{re.escape(sku)}\s*$",
            re.IGNORECASE
        )

        nombre = patron.sub("", nombre).strip()

    return nombre


def obtener_titulo(soup):
    """
    Obtiene el título real del producto.
    """

    selectores = [
        "h1.product_title",
        "h1.entry-title",
        "h1",
    ]

    for selector in selectores:
        elemento = soup.select_one(selector)

        if elemento:
            texto = elemento.get_text(" ", strip=True)

            if texto:
                return texto

    return None


def obtener_sku_desde_pagina(soup):
    """
    Busca el SKU en los lugares habituales de WooCommerce.
    """

    # --------------------------------------------------------
    # 1. Selector típico de WooCommerce
    # --------------------------------------------------------

    selectores = [
        ".sku",
        ".product_meta .sku",
        "[itemprop='sku']",
    ]

    for selector in selectores:

        elemento = soup.select_one(selector)

        if elemento:

            texto = elemento.get_text(" ", strip=True)

            sku = extraer_sku(texto)

            if sku:
                return sku

            # Algunos sitios ponen directamente:
            # 50774
            if texto.isdigit():
                return f"SKU{texto}"

    # --------------------------------------------------------
    # 2. Buscar "SKU" en el texto de metadatos
    # --------------------------------------------------------

    meta = soup.select_one(".product_meta")

    if meta:

        texto = meta.get_text(" ", strip=True)

        sku = extraer_sku(texto)

        if sku:
            return sku

    # --------------------------------------------------------
    # 3. Buscar SKU en todo el HTML
    # --------------------------------------------------------

    html = str(soup)

    sku = extraer_sku(html)

    if sku:
        return sku

    return None


def extraer_sku_desde_url(url):
    """
    Como respaldo, intenta obtener el SKU desde la URL.

    Ejemplo:
    /producto/anillos-sku50774/

    -> SKU50774
    """

    return extraer_sku(url)


def procesar_producto(producto, session):
    """
    Procesa un producto individual.
    """

    nombre_actual = producto.get("nombre")
    sku_actual = producto.get("sku")
    url = producto.get("url")

    # ========================================================
    # PRIMERO: intentar sacar SKU del nombre existente
    # ========================================================

    sku = sku_actual or extraer_sku(nombre_actual)

    if sku:

        producto["sku"] = sku

        # Limpiar SKU pegado al nombre
        producto["nombre"] = limpiar_nombre(
            nombre_actual,
            sku
        )

        return producto, False, "SKU encontrado localmente"

    # ========================================================
    # SEGUNDO: intentar sacar SKU de la URL
    # ========================================================

    sku_url = extraer_sku_desde_url(url)

    if sku_url:

        producto["sku"] = sku_url

        producto["nombre"] = limpiar_nombre(
            nombre_actual,
            sku_url
        )

        return producto, False, "SKU encontrado en URL"

    # ========================================================
    # TERCERO: consultar página del producto
    # ========================================================

    if not url:
        return producto, True, "Producto sin URL"

    try:

        print(f"   Consultando: {url}")

        response = session.get(
            url,
            headers=HEADERS,
            timeout=30
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "lxml"
        )

        # ----------------------------------------------------
        # SKU
        # ----------------------------------------------------

        sku_pagina = obtener_sku_desde_pagina(soup)

        if sku_pagina:
            producto["sku"] = sku_pagina

        # ----------------------------------------------------
        # NOMBRE REAL
        # ----------------------------------------------------

        titulo = obtener_titulo(soup)

        if titulo:

            # Si el título trae SKU, también lo extraemos
            sku_titulo = extraer_sku(titulo)

            if not producto.get("sku") and sku_titulo:
                producto["sku"] = sku_titulo

            producto["nombre"] = limpiar_nombre(
                titulo,
                producto.get("sku")
            )

        return producto, False, "Página procesada"

    except Exception as e:

        print(f"   ERROR: {e}")

        return producto, True, str(e)


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    print("=" * 70)
    print(" COMPLETAR SKUs - MURANO STEEL")
    print("=" * 70)

    # --------------------------------------------------------
    # Verificar JSON
    # --------------------------------------------------------

    if not JSON_PATH.exists():

        print()
        print(f"ERROR: No se encontró:")
        print(JSON_PATH)
        return

    # --------------------------------------------------------
    # Crear respaldo
    # --------------------------------------------------------

    shutil.copy2(
        JSON_PATH,
        BACKUP_PATH
    )

    print()
    print("✓ Respaldo creado:")
    print(BACKUP_PATH)

    # --------------------------------------------------------
    # Cargar catálogo
    # --------------------------------------------------------

    with open(
        JSON_PATH,
        "r",
        encoding="utf-8"
    ) as archivo:

        catalogo = json.load(archivo)

    print()
    print(f"Productos cargados: {len(catalogo)}")

    # --------------------------------------------------------
    # Estadísticas iniciales
    # --------------------------------------------------------

    skus_nulos_iniciales = sum(
        1
        for producto in catalogo
        if not producto.get("sku")
    )

    print(
        f"Productos inicialmente sin SKU: "
        f"{skus_nulos_iniciales}"
    )

    # --------------------------------------------------------
    # Sesión HTTP
    # --------------------------------------------------------

    session = requests.Session()

    procesados = 0
    encontrados = 0
    errores = 0
    consultas_web = 0

    # ========================================================
    # PROCESAR
    # ========================================================

    for indice, producto in enumerate(catalogo, start=1):

        sku_antes = producto.get("sku")

        # ----------------------------------------------------
        # Solo procesamos productos sin SKU
        # ----------------------------------------------------

        if sku_antes:
            continue

        print()
        print(
            f"[{indice}/{len(catalogo)}] "
            f"{producto.get('nombre')}"
        )

        producto_actualizado, error, mensaje = procesar_producto(
            producto,
            session
        )

        catalogo[indice - 1] = producto_actualizado

        procesados += 1

        if "Página procesada" in mensaje:
            consultas_web += 1

        if producto_actualizado.get("sku"):

            encontrados += 1

            print(
                f"   ✓ SKU: "
                f"{producto_actualizado.get('sku')}"
            )

            print(
                f"   ✓ Nombre: "
                f"{producto_actualizado.get('nombre')}"
            )

        else:

            print("   ⚠ SKU no encontrado")

        if error:
            errores += 1

        time.sleep(DELAY_BETWEEN_REQUESTS)

    # ========================================================
    # GUARDAR
    # ========================================================

    with open(
        JSON_PATH,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            catalogo,
            archivo,
            ensure_ascii=False,
            indent=2
        )

    # ========================================================
    # ESTADÍSTICAS FINALES
    # ========================================================

    skus_nulos_finales = sum(
        1
        for producto in catalogo
        if not producto.get("sku")
    )

    print()
    print("=" * 70)
    print(" PROCESO FINALIZADO")
    print("=" * 70)

    print(f"Total productos:              {len(catalogo)}")
    print(f"Productos procesados:         {procesados}")
    print(f"SKUs encontrados:             {encontrados}")
    print(f"Consultas web realizadas:     {consultas_web}")
    print(f"Errores:                      {errores}")
    print(f"Productos sin SKU restantes:  {skus_nulos_finales}")

    print()
    print(f"✓ Catálogo actualizado:")
    print(JSON_PATH)

    print()
    print(f"✓ Respaldo:")
    print(BACKUP_PATH)

    print("=" * 70)


if __name__ == "__main__":
    main()