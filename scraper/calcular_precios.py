import json
import shutil
from pathlib import Path


# ============================================================
# CONFIGURACIÓN
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

JSON_PATH = BASE_DIR / "catalogo.json"
BACKUP_PATH = BASE_DIR / "catalogo_backup_antes_precios.json"


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    print("=" * 70)
    print(" CALCULAR PRECIO DE VENTA - TU ESENCIA")
    print("=" * 70)

    # --------------------------------------------------------
    # Verificar que exista catalogo.json
    # --------------------------------------------------------

    if not JSON_PATH.exists():

        print()
        print("ERROR: No se encontró el archivo:")
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
    # Contadores
    # --------------------------------------------------------

    productos_sin_descuento = 0
    productos_con_descuento = 0
    errores = 0

    # Para mostrar ejemplos
    ejemplos = []

    # ========================================================
    # CALCULAR PRECIO DE VENTA
    # ========================================================

    for producto in catalogo:

        try:

            precio = producto.get("precio")
            precio_anterior = producto.get("precio_anterior")
            en_descuento = producto.get("en_descuento")

            # ------------------------------------------------
            # PRODUCTO SIN DESCUENTO
            # precio_venta = precio × 2
            # ------------------------------------------------

            if en_descuento is False:

                if precio is None:
                    raise ValueError(
                        "Producto sin precio"
                    )

                precio_venta = precio * 2

                productos_sin_descuento += 1

                if len(ejemplos) < 3:
                    ejemplos.append({
                        "nombre": producto.get("nombre"),
                        "tipo": "Sin descuento",
                        "calculo": f"{precio} × 2",
                        "precio_venta": precio_venta
                    })

            # ------------------------------------------------
            # PRODUCTO CON DESCUENTO
            # precio_venta = precio_anterior × 3
            # ------------------------------------------------

            elif en_descuento is True:

                if precio_anterior is None:
                    raise ValueError(
                        "Producto con descuento pero sin precio_anterior"
                    )

                precio_venta = precio_anterior * 3

                productos_con_descuento += 1

                if len(ejemplos) < 6:
                    ejemplos.append({
                        "nombre": producto.get("nombre"),
                        "tipo": "Con descuento",
                        "calculo": f"{precio_anterior} × 3",
                        "precio_venta": precio_venta
                    })

            # ------------------------------------------------
            # VALOR NO VÁLIDO
            # ------------------------------------------------

            else:

                raise ValueError(
                    f"en_descuento tiene valor inesperado: "
                    f"{en_descuento}"
                )

            # ------------------------------------------------
            # Guardar precio de venta
            # ------------------------------------------------

            producto["precio_venta"] = precio_venta

        except Exception as e:

            errores += 1

            print()
            print(
                f"⚠ ERROR en producto: "
                f"{producto.get('nombre')}"
            )

            print(f"   {e}")

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
    # RESULTADO
    # ========================================================

    print()
    print("=" * 70)
    print(" PROCESO FINALIZADO")
    print("=" * 70)

    print(
        f"Total productos:              {len(catalogo)}"
    )

    print(
        f"Sin descuento (×2):           "
        f"{productos_sin_descuento}"
    )

    print(
        f"Con descuento (×3):           "
        f"{productos_con_descuento}"
    )

    print(
        f"Errores:                       {errores}"
    )

    print()

    # --------------------------------------------------------
    # Mostrar ejemplos
    # --------------------------------------------------------

    print("EJEMPLOS:")

    for ejemplo in ejemplos:

        print()
        print(f"Producto: {ejemplo['nombre']}")
        print(f"Tipo:     {ejemplo['tipo']}")
        print(f"Cálculo:  {ejemplo['calculo']}")
        print(f"Venta:    ${ejemplo['precio_venta']:,}")

    print()
    print("✓ Catálogo actualizado:")
    print(JSON_PATH)

    print()
    print("✓ Respaldo:")
    print(BACKUP_PATH)

    print("=" * 70)


if __name__ == "__main__":
    main()