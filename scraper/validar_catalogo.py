import json
from collections import Counter


ARCHIVO = "catalogo.json"


# ============================================================
# CARGAR CATÁLOGO
# ============================================================

with open(ARCHIVO, "r", encoding="utf-8") as f:
    productos = json.load(f)


print("=" * 80)
print("VALIDACIÓN ESTADÍSTICA FINAL DEL CATÁLOGO")
print("=" * 80)


# ============================================================
# 1. CANTIDAD TOTAL
# ============================================================

print("\n[1] CANTIDAD DE PRODUCTOS")

total = len(productos)

print(f"Total productos: {total}")


# ============================================================
# 2. VALIDACIÓN DE IDS
# ============================================================

print("\n[2] VALIDACIÓN DE IDs")

ids = [p.get("id") for p in productos]

ids_validos = all(isinstance(i, int) for i in ids)
ids_unicos = len(set(ids)) == len(ids)

ids_esperados = list(range(1, total + 1))
secuencia_correcta = ids == ids_esperados

print(f"IDs enteros: {'OK' if ids_validos else 'ERROR'}")
print(f"IDs únicos: {'OK' if ids_unicos else 'ERROR'}")
print(f"Secuencia 1-{total}: {'OK' if secuencia_correcta else 'ERROR'}")


# ============================================================
# 3. CAMPOS PRINCIPALES
# ============================================================

print("\n[3] CAMPOS PRINCIPALES")

campos_requeridos = [
    "id",
    "nombre",
    "slug",
    "sku",
    "precio",
    "precio_anterior",
    "en_descuento",
    "moneda",
    "categoria",
    "url",
    "imagen",
    "imagen_alta",
    "precio_venta",
    "atributos"
]

for campo in campos_requeridos:

    faltantes = sum(
        1 for p in productos
        if campo not in p
    )

    print(
        f"{campo:20} "
        f"{'OK' if faltantes == 0 else f'FALTAN {faltantes}'}"
    )


# ============================================================
# 4. DUPLICADOS DE URL
# ============================================================

print("\n[4] DUPLICADOS DE URL")

urls = [p.get("url") for p in productos]

duplicadas_url = [
    url
    for url, cantidad in Counter(urls).items()
    if cantidad > 1
]

print(f"URLs duplicadas: {len(duplicadas_url)}")

if duplicadas_url:
    for url in duplicadas_url:
        print(f"  {url}")


# ============================================================
# 5. DUPLICADOS DE SKU
# ============================================================

print("\n[5] DUPLICADOS DE SKU")

skus = [
    p.get("sku")
    for p in productos
    if p.get("sku")
]

conteo_sku = Counter(skus)

duplicados_sku = {
    sku: cantidad
    for sku, cantidad in conteo_sku.items()
    if cantidad > 1
}

print(f"SKUs únicos: {len(conteo_sku)}")
print(f"SKUs duplicados: {len(duplicados_sku)}")

if duplicados_sku:
    print("\nSKUs repetidos:")

    for sku, cantidad in sorted(duplicados_sku.items()):
        print(f"  {sku}: {cantidad}")


# ============================================================
# 6. CATEGORÍAS
# ============================================================

print("\n[6] CATEGORÍAS")

categorias = Counter(
    p.get("categoria")
    for p in productos
)

for categoria, cantidad in categorias.most_common():
    porcentaje = cantidad / total * 100

    print(
        f"{categoria:20} "
        f"{cantidad:4} "
        f"({porcentaje:6.2f}%)"
    )


# ============================================================
# 7. ATRIBUTOS
# ============================================================

print("\n[7] ATRIBUTOS")

atributos_permitidos = {
    "tipo",
    "color",
    "estilo",
    "material"
}

valores = {
    "tipo": Counter(),
    "color": Counter(),
    "estilo": Counter(),
    "material": Counter()
}

productos_sin_atributos = 0

for producto in productos:

    atributos = producto.get("atributos", {})

    tiene_atributo = False

    for campo in atributos_permitidos:

        valor = atributos.get(campo)

        if valor is not None:
            valores[campo][valor] += 1
            tiene_atributo = True

    if not tiene_atributo:
        productos_sin_atributos += 1


# ============================================================
# 8. VALORES POR ATRIBUTO
# ============================================================

for campo in [
    "tipo",
    "color",
    "estilo",
    "material"
]:

    print(f"\n--- {campo.upper()} ---")

    contador = valores[campo]

    if not contador:
        print("Sin valores")
        continue

    for valor, cantidad in contador.most_common():

        porcentaje = cantidad / total * 100

        print(
            f"{str(valor):20} "
            f"{cantidad:4} "
            f"({porcentaje:6.2f}%)"
        )


# ============================================================
# 9. PRODUCTOS SIN ATRIBUTOS
# ============================================================

print("\n[8] PRODUCTOS SIN ATRIBUTOS")

print(
    f"Sin ningún atributo: "
    f"{productos_sin_atributos}"
)

print(
    f"Con al menos un atributo: "
    f"{total - productos_sin_atributos}"
)


# ============================================================
# 10. ATRIBUTOS DESCONOCIDOS
# ============================================================

print("\n[9] ATRIBUTOS DESCONOCIDOS")

atributos_desconocidos = set()

for producto in productos:

    atributos = producto.get("atributos", {})

    for campo in atributos.keys():

        if campo not in atributos_permitidos:
            atributos_desconocidos.add(campo)


if atributos_desconocidos:
    print("ERROR - atributos no permitidos:")

    for atributo in sorted(atributos_desconocidos):
        print(f"  {atributo}")

else:
    print("OK - solo existen los atributos permitidos")


# ============================================================
# 11. VALORES VACÍOS
# ============================================================

print("\n[10] VALORES VACÍOS")

for campo in atributos_permitidos:

    vacios = 0

    for producto in productos:

        valor = producto.get("atributos", {}).get(campo)

        if valor == "":
            vacios += 1

    print(
        f"{campo:10}: "
        f"{'OK' if vacios == 0 else f'{vacios} vacíos'}"
    )


# ============================================================
# 12. CONSISTENCIA DE TIPOS DE DATOS
# ============================================================

print("\n[11] CONSISTENCIA DE TIPOS")

errores_tipo = []

for producto in productos:

    atributos = producto.get("atributos", {})

    for campo in atributos_permitidos:

        valor = atributos.get(campo)

        if valor is not None and not isinstance(valor, str):

            errores_tipo.append(
                (
                    producto.get("id"),
                    campo,
                    valor
                )
            )


if errores_tipo:

    print(
        f"ERROR - {len(errores_tipo)} valores "
        f"con tipo incorrecto"
    )

    for error in errores_tipo:
        print(error)

else:

    print(
        "OK - todos los atributos son "
        "string o null"
    )


# ============================================================
# RESUMEN FINAL
# ============================================================

print("\n" + "=" * 80)
print("RESUMEN FINAL")
print("=" * 80)

print(f"Productos:              {total}")
print(f"URLs duplicadas:        {len(duplicadas_url)}")
print(f"SKUs únicos:            {len(conteo_sku)}")
print(f"SKUs duplicados:        {len(duplicados_sku)}")
print(f"Sin atributos:          {productos_sin_atributos}")
print(
    f"Con atributos:          "
    f"{total - productos_sin_atributos}"
)

print("\nValidación terminada.")