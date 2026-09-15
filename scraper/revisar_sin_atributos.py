import json

ARCHIVO = "catalogo.json"

with open(ARCHIVO, "r", encoding="utf-8") as f:
    productos = json.load(f)

sin_atributos = []

for p in productos:
    atributos = p.get("atributos", {})

    if all(valor is None for valor in atributos.values()):
        sin_atributos.append(p)

print("=" * 80)
print(f"PRODUCTOS SIN ATRIBUTOS: {len(sin_atributos)}")
print("=" * 80)

for p in sin_atributos:
    print(
        f"\nID: {p.get('id')}"
        f"\nNombre: {p.get('nombre')}"
        f"\nSKU: {p.get('sku')}"
        f"\nCategoría: {p.get('categoria')}"
        f"\nURL: {p.get('url')}"
        f"\nAtributos: {p.get('atributos')}"
    )
    print("-" * 80)