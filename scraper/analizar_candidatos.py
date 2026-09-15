import json
import re
from pathlib import Path
from collections import Counter


# ============================================================
# RUTAS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CATALOGO = BASE_DIR / "catalogo.json"
REPORTE_ENRIQUECIMIENTO = BASE_DIR / "reporte_enriquecimiento.json"
REPORTE_CANDIDATOS = BASE_DIR / "reporte_candidatos.json"


# ============================================================
# NORMALIZACIÓN
# ============================================================

def normalizar_texto(texto):
    if not texto:
        return ""

    texto = texto.lower()

    # Eliminar SKU
    texto = re.sub(r"sku\d+", " ", texto)

    # Separadores
    texto = re.sub(r"[-_/]", " ", texto)

    # Eliminar caracteres especiales
    texto = re.sub(r"[^a-záéíóúüñ0-9\s]", " ", texto)

    # Espacios múltiples
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto


# ============================================================
# PALABRAS QUE NO QUEREMOS COMO ATRIBUTOS
# ============================================================

PALABRAS_IGNORAR = {
    # Categorías / términos generales
    "aretes",
    "anillos",
    "anillo",
    "pulseras",
    "pulsera",
    "candongas",
    "cadenas",
    "juegos",
    "juego",
    "dijes",
    "dije",
    "coleros",
    "pelo",
    "otros",

    # Materiales ya detectados
    "acero",
    "plastimetal",
    "cover",
    "gold",
    "rodio",

    # Colores ya detectados
    "dorado",
    "plateado",
    "plateaado",

    # Palabras comerciales
    "unidad",
    "pares",
    "kit",
    "precio",
    "emprendimiento",
    "ensamble",

    # Medidas / cantidades
    "mm",
    "x12",
    "3mm",
    "4mm",
    "5mm",
    "6mm",
    "8mm",
    "20mm",
    "25mm",
    "30mm",
    "40mm",
    "45mm",
    "50mm",
    "60mm",
    "65mm",
    "70mm",

    # Errores / ruido conocidos
    "sku",
}


# ============================================================
# EXTRAER PALABRAS
# ============================================================

def extraer_palabras(texto):

    palabras = []

    for palabra in texto.split():

        palabra = palabra.strip()

        if len(palabra) < 3:
            continue

        if palabra.isdigit():
            continue

        if palabra in PALABRAS_IGNORAR:
            continue

        # Ignorar medidas como 30mm
        if re.match(r"^\d+mm$", palabra):
            continue

        palabras.append(palabra)

    return palabras


# ============================================================
# MAIN
# ============================================================

def main():

    print("========================================")
    print("       ANÁLISIS DE CANDIDATOS")
    print("========================================")

    if not CATALOGO.exists():
        print("\nERROR: No se encontró catalogo.json")
        return

    # --------------------------------------------------------
    # Leer catálogo
    # --------------------------------------------------------

    with open(CATALOGO, "r", encoding="utf-8") as f:
        catalogo = json.load(f)

    print(f"\nProductos encontrados: {len(catalogo)}")

    # --------------------------------------------------------
    # Productos sin atributos
    # --------------------------------------------------------

    sin_atributos = []

    for producto in catalogo:

        atributos = producto.get("atributos", {})

        if not any(atributos.values()):

            sin_atributos.append({
                "id": producto.get("id"),
                "nombre": producto.get("nombre"),
                "slug": producto.get("slug"),
                "categoria": producto.get("categoria"),
            })

    print(f"Productos sin atributos: {len(sin_atributos)}")

    # --------------------------------------------------------
    # Analizar palabras de TODO el catálogo
    # --------------------------------------------------------

    contador_global = Counter()

    contador_categoria = {}

    for producto in catalogo:

        nombre = producto.get("nombre") or ""
        slug = producto.get("slug") or ""
        categoria = producto.get("categoria") or "sin-categoria"

        texto = normalizar_texto(
            f"{nombre} {slug}"
        )

        palabras = extraer_palabras(texto)

        for palabra in palabras:
            contador_global[palabra] += 1

        if categoria not in contador_categoria:
            contador_categoria[categoria] = Counter()

        for palabra in palabras:
            contador_categoria[categoria][palabra] += 1

    # --------------------------------------------------------
    # Mostrar productos sin atributos
    # --------------------------------------------------------

    print("\n========================================")
    print("PRODUCTOS SIN ATRIBUTOS")
    print("========================================")

    for producto in sin_atributos:

        print(
            f"\nID: {producto['id']}"
        )

        print(
            f"Nombre: {producto['nombre']}"
        )

        print(
            f"Slug: {producto['slug']}"
        )

        print(
            f"Categoría: {producto['categoria']}"
        )

    # --------------------------------------------------------
    # Mostrar candidatos
    # --------------------------------------------------------

    print("\n========================================")
    print("CANDIDATOS NO CLASIFICADOS")
    print("========================================")

    for palabra, cantidad in contador_global.most_common(150):

        print(
            f"{palabra:<30} {cantidad}"
        )

    # --------------------------------------------------------
    # Candidatos por categoría
    # --------------------------------------------------------

    print("\n========================================")
    print("CANDIDATOS POR CATEGORÍA")
    print("========================================")

    for categoria in sorted(contador_categoria):

        print(f"\n--- {categoria} ---")

        for palabra, cantidad in contador_categoria[categoria].most_common(50):

            print(
                f"{palabra:<30} {cantidad}"
            )

    # --------------------------------------------------------
    # Guardar reporte
    # --------------------------------------------------------

    reporte = {
        "total_productos": len(catalogo),

        "productos_sin_atributos": sin_atributos,

        "palabras_candidatas": [
            {
                "palabra": palabra,
                "cantidad": cantidad
            }
            for palabra, cantidad in contador_global.most_common(200)
        ],

        "palabras_por_categoria": {
            categoria: [
                {
                    "palabra": palabra,
                    "cantidad": cantidad
                }
                for palabra, cantidad in contador.most_common(100)
            ]
            for categoria, contador in contador_categoria.items()
        }
    }

    with open(REPORTE_CANDIDATOS, "w", encoding="utf-8") as f:

        json.dump(
            reporte,
            f,
            ensure_ascii=False,
            indent=2
        )

    print("\n========================================")
    print("ANÁLISIS TERMINADO")
    print("========================================")

    print(
        f"\nReporte generado:\n{REPORTE_CANDIDATOS}"
    )


if __name__ == "__main__":
    main()