import json
import re
from pathlib import Path
from collections import Counter

BASE_DIR = Path(__file__).resolve().parent.parent
CATALOGO = BASE_DIR / "catalogo.json"


def limpiar_texto(texto):
    if not texto:
        return ""

    texto = texto.lower()

    # Eliminar SKU
    texto = re.sub(r"sku\d+", " ", texto)

    # Reemplazar separadores
    texto = re.sub(r"[-_/]", " ", texto)

    # Eliminar caracteres especiales
    texto = re.sub(r"[^a-záéíóúüñ0-9\s]", " ", texto)

    # Espacios múltiples
    texto = re.sub(r"\s+", " ", texto).strip()

    return texto


def main():

    print("========================================")
    print("       ANÁLISIS DE ATRIBUTOS")
    print("========================================")

    if not CATALOGO.exists():
        print(f"\nERROR: No existe:")
        print(CATALOGO)
        return

    with open(CATALOGO, "r", encoding="utf-8") as f:
        catalogo = json.load(f)

    print(f"\nProductos encontrados: {len(catalogo)}")

    palabras = Counter()
    palabras_por_categoria = {}

    for producto in catalogo:

        nombre = producto.get("nombre") or ""
        slug = producto.get("slug") or ""
        categoria = producto.get("categoria") or "sin-categoria"

        texto = limpiar_texto(f"{nombre} {slug}")

        tokens = texto.split()

        # Contar palabras
        for palabra in tokens:
            if len(palabra) >= 3:
                palabras[palabra] += 1

        # Contar por categoría
        if categoria not in palabras_por_categoria:
            palabras_por_categoria[categoria] = Counter()

        for palabra in tokens:
            if len(palabra) >= 3:
                palabras_por_categoria[categoria][palabra] += 1

    # -------------------------------------------------
    # PALABRAS MÁS FRECUENTES
    # -------------------------------------------------

    print("\n========================================")
    print("PALABRAS MÁS FRECUENTES")
    print("========================================")

    for palabra, cantidad in palabras.most_common(100):
        print(f"{palabra:<30} {cantidad}")

    # -------------------------------------------------
    # PALABRAS POR CATEGORÍA
    # -------------------------------------------------

    print("\n========================================")
    print("PALABRAS POR CATEGORÍA")
    print("========================================")

    for categoria in sorted(palabras_por_categoria):

        print(f"\n--- {categoria} ---")

        for palabra, cantidad in palabras_por_categoria[categoria].most_common(30):
            print(f"{palabra:<30} {cantidad}")

    # -------------------------------------------------
    # GUARDAR REPORTE
    # -------------------------------------------------

    reporte = {
        "total_productos": len(catalogo),
        "palabras_mas_frecuentes": [
            {
                "palabra": palabra,
                "cantidad": cantidad
            }
            for palabra, cantidad in palabras.most_common(200)
        ],
        "palabras_por_categoria": {
            categoria: [
                {
                    "palabra": palabra,
                    "cantidad": cantidad
                }
                for palabra, cantidad in contador.most_common(100)
            ]
            for categoria, contador in palabras_por_categoria.items()
        }
    }

    archivo_reporte = BASE_DIR / "reporte_atributos.json"

    with open(archivo_reporte, "w", encoding="utf-8") as f:
        json.dump(
            reporte,
            f,
            ensure_ascii=False,
            indent=2
        )

    print("\n========================================")
    print("ANÁLISIS TERMINADO")
    print("========================================")
    print(f"Reporte generado:")
    print(archivo_reporte)


if __name__ == "__main__":
    main()