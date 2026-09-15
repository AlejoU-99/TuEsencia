import json
import re
import shutil
from pathlib import Path
from collections import Counter


# ============================================================
# RUTAS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CATALOGO = BASE_DIR / "catalogo.json"
BACKUP = BASE_DIR / "catalogo_backup_antes_enriquecimiento_v2.json"
REPORTE = BASE_DIR / "reporte_enriquecimiento_v2.json"


# ============================================================
# NORMALIZACIÓN DEL TEXTO
# ============================================================

def normalizar_texto(texto):
    """
    Normaliza el texto para facilitar la detección de atributos.

    No modifica el nombre ni el slug original del producto.
    """

    if not texto:
        return ""

    texto = texto.lower()

    # --------------------------------------------------------
    # Separar palabras pegadas a SKU
    #
    # Ejemplo:
    # dijeSKU30501 -> dije SKU30501
    # aretesSKU12061 -> aretes SKU12061
    # --------------------------------------------------------

    texto = re.sub(r"([a-záéíóúüñ])sku", r"\1 sku", texto)

    # --------------------------------------------------------
    # Eliminar SKU
    # --------------------------------------------------------

    texto = re.sub(r"\bsku\d+\b", " ", texto)

    # --------------------------------------------------------
    # Normalizaciones conocidas
    # --------------------------------------------------------

    texto = texto.replace("plateaado", "plateado")
    texto = texto.replace("inciciales", "iniciales")
    texto = texto.replace("jugeos", "juegos")

    # Singular → forma estándar
    texto = re.sub(r"\banillo\b", "anillos", texto)
    texto = re.sub(r"\bpulsera\b", "pulseras", texto)
    texto = re.sub(r"\bjuego\b", "juegos", texto)
    texto = re.sub(r"\bdije\b", "dijes", texto)
    texto = re.sub(r"\bperla\b", "perlas", texto)

    # Separadores
    texto = re.sub(r"[-_/]", " ", texto)

    # Caracteres especiales
    texto = re.sub(
        r"[^a-záéíóúüñ0-9\s]",
        " ",
        texto
    )

    # Espacios múltiples
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto


def contiene_palabra(texto, palabra):
    """
    Busca una palabra completa.
    Evita falsos positivos por coincidencias parciales.
    """

    return re.search(
        rf"\b{re.escape(palabra)}\b",
        texto,
        flags=re.IGNORECASE
    ) is not None


# ============================================================
# TIPOS
# ============================================================

TIPOS = [
    "aretes",
    "anillos",
    "pulseras",
    "candongas",
    "cadenas",
    "juegos",
    "dijes",
    "coleros",
    "earcuff",
    "cuff",
    "topo",
]


# ============================================================
# COLORES
# ============================================================

COLORES = [
    "dorado",
    "plateado",
    "rodio",
]


# ============================================================
# MATERIALES / ACABADOS
# ============================================================

MATERIALES = [
    "cover gold",
    "acero",
    "plastimetal",
    "rodio",
]


# ============================================================
# ESTILOS / DISEÑOS
# ============================================================

ESTILOS = [
    "bolas chicle",
    "perlas",
    "camandula",
    "relicario",
    "iniciales",
]


# ============================================================
# DETECTAR TIPO
# ============================================================

def detectar_tipo(texto):

    # --------------------------------------------------------
    # Caso especial:
    #
    # ear + cuff
    #
    # Se considera earcuff.
    # --------------------------------------------------------

    if (
        contiene_palabra(texto, "ear")
        and contiene_palabra(texto, "cuff")
    ):
        return "earcuff"

    # --------------------------------------------------------
    # earcuff escrito directamente
    # --------------------------------------------------------

    if contiene_palabra(texto, "earcuff"):
        return "earcuff"

    # --------------------------------------------------------
    # Prioridad de tipos específicos
    # --------------------------------------------------------

    prioridades = [
        "cuff",
        "topo",
        "candongas",
        "aretes",
        "anillos",
        "pulseras",
        "cadenas",
        "dijes",
        "coleros",
        "juegos",
    ]

    for tipo in prioridades:

        if contiene_palabra(texto, tipo):
            return tipo

    return None


# ============================================================
# DETECTAR COLOR
# ============================================================

def detectar_color(texto):

    # Orden explícito
    for color in COLORES:

        if contiene_palabra(texto, color):

            if color == "plateado":
                return "plateado"

            return color

    return None


# ============================================================
# DETECTAR MATERIAL
# ============================================================

def detectar_material(texto):

    # Cover Gold
    if (
        contiene_palabra(texto, "cover")
        and contiene_palabra(texto, "gold")
    ):
        return "cover gold"

    # Acero
    if contiene_palabra(texto, "acero"):
        return "acero"

    # Plastimetal
    if contiene_palabra(texto, "plastimetal"):
        return "plastimetal"

    # Rodio
    if contiene_palabra(texto, "rodio"):
        return "rodio"

    return None


# ============================================================
# DETECTAR ESTILO
# ============================================================

def detectar_estilo(texto):

    # --------------------------------------------------------
    # Bolas + chicle
    #
    # Ambos deben aparecer para clasificar como
    # "bolas chicle".
    # --------------------------------------------------------

    if (
        contiene_palabra(texto, "bolas")
        and contiene_palabra(texto, "chicle")
    ):
        return "bolas chicle"

    # --------------------------------------------------------
    # Otros estilos conocidos
    # --------------------------------------------------------

    if contiene_palabra(texto, "perlas"):
        return "perlas"

    if contiene_palabra(texto, "camandula"):
        return "camandula"

    if contiene_palabra(texto, "relicario"):
        return "relicario"

    if contiene_palabra(texto, "iniciales"):
        return "iniciales"

    return None


# ============================================================
# PROCESAMIENTO PRINCIPAL
# ============================================================

def main():

    print("========================================")
    print("   ENRIQUECIMIENTO DEL CATÁLOGO V2")
    print("========================================")

    # --------------------------------------------------------
    # Validar catálogo
    # --------------------------------------------------------

    if not CATALOGO.exists():

        print("\nERROR:")
        print("No se encontró:")
        print(CATALOGO)

        return

    # --------------------------------------------------------
    # Leer catálogo
    # --------------------------------------------------------

    with open(CATALOGO, "r", encoding="utf-8") as f:
        catalogo = json.load(f)

    if not isinstance(catalogo, list):

        print("\nERROR:")
        print("El catálogo no contiene una lista.")

        return

    print(f"\nProductos encontrados: {len(catalogo)}")

    # --------------------------------------------------------
    # Crear backup
    # --------------------------------------------------------

    shutil.copy2(CATALOGO, BACKUP)

    print("\nBackup creado:")
    print(BACKUP)

    # --------------------------------------------------------
    # Estadísticas
    # --------------------------------------------------------

    estadisticas = {
        "tipo": Counter(),
        "color": Counter(),
        "estilo": Counter(),
        "material": Counter(),
    }

    sin_atributos = []

    # --------------------------------------------------------
    # Procesar productos
    # --------------------------------------------------------

    for producto in catalogo:

        nombre = producto.get("nombre") or ""
        slug = producto.get("slug") or ""
        categoria = producto.get("categoria") or ""

        # ----------------------------------------------------
        # Fuente para detectar atributos
        # ----------------------------------------------------

        texto_original = (
            f"{nombre} {slug} {categoria}"
        )

        texto = normalizar_texto(texto_original)

        # ----------------------------------------------------
        # Detectar
        # ----------------------------------------------------

        tipo = detectar_tipo(texto)
        color = detectar_color(texto)
        estilo = detectar_estilo(texto)
        material = detectar_material(texto)

        # ----------------------------------------------------
        # Crear atributos
        # ----------------------------------------------------

        atributos = {
            "tipo": tipo,
            "color": color,
            "estilo": estilo,
            "material": material,
        }

        producto["atributos"] = atributos

        # ----------------------------------------------------
        # Estadísticas
        # ----------------------------------------------------

        if tipo:
            estadisticas["tipo"][tipo] += 1

        if color:
            estadisticas["color"][color] += 1

        if estilo:
            estadisticas["estilo"][estilo] += 1

        if material:
            estadisticas["material"][material] += 1

        # ----------------------------------------------------
        # Sin atributos
        # ----------------------------------------------------

        if not any(atributos.values()):

            sin_atributos.append({
                "id": producto.get("id"),
                "nombre": nombre,
                "slug": slug,
                "categoria": categoria,
            })

    # --------------------------------------------------------
    # Guardar catálogo
    # --------------------------------------------------------

    with open(CATALOGO, "w", encoding="utf-8") as f:

        json.dump(
            catalogo,
            f,
            ensure_ascii=False,
            indent=2
        )

    # --------------------------------------------------------
    # Crear reporte
    # --------------------------------------------------------

    reporte = {

        "total_productos": len(catalogo),

        "estadisticas": {
            "tipo": dict(
                estadisticas["tipo"]
            ),

            "color": dict(
                estadisticas["color"]
            ),

            "estilo": dict(
                estadisticas["estilo"]
            ),

            "material": dict(
                estadisticas["material"]
            ),
        },

        "productos_sin_atributos": sin_atributos,
    }

    with open(REPORTE, "w", encoding="utf-8") as f:

        json.dump(
            reporte,
            f,
            ensure_ascii=False,
            indent=2
        )

    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    print("\n========================================")
    print("             RESULTADO V2")
    print("========================================")

    print(
        f"\nProductos procesados: {len(catalogo)}"
    )

    print("\nTIPOS:")

    for valor, cantidad in estadisticas["tipo"].most_common():

        print(
            f"  {valor:<20} {cantidad}"
        )

    print("\nCOLORES:")

    for valor, cantidad in estadisticas["color"].most_common():

        print(
            f"  {valor:<20} {cantidad}"
        )

    print("\nESTILOS:")

    for valor, cantidad in estadisticas["estilo"].most_common():

        print(
            f"  {valor:<20} {cantidad}"
        )

    print("\nMATERIALES:")

    for valor, cantidad in estadisticas["material"].most_common():

        print(
            f"  {valor:<20} {cantidad}"
        )

    print("\nPRODUCTOS SIN ATRIBUTOS:")

    print(
        f"  {len(sin_atributos)}"
    )

    print("\nReporte generado:")

    print(REPORTE)

    print("\n========================================")
    print("     ENRIQUECIMIENTO V2 TERMINADO")
    print("========================================")


if __name__ == "__main__":
    main()