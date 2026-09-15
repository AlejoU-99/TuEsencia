import json
import shutil
from pathlib import Path

# Rutas
BASE_DIR = Path(__file__).resolve().parent.parent
CATALOGO = BASE_DIR / "catalogo.json"
BACKUP = BASE_DIR / "catalogo_backup_antes_ids.json"


def main():
    print("========================================")
    print("       AGREGAR ID AL CATÁLOGO")
    print("========================================")

    # Validar que exista el catálogo
    if not CATALOGO.exists():
        print(f"\nERROR: No se encontró:")
        print(CATALOGO)
        return

    # Crear backup
    shutil.copy2(CATALOGO, BACKUP)
    print(f"\nBackup creado:")
    print(BACKUP)

    # Leer catálogo
    with open(CATALOGO, "r", encoding="utf-8") as f:
        catalogo = json.load(f)

    if not isinstance(catalogo, list):
        print("\nERROR: El catálogo no contiene una lista de productos.")
        return

    print(f"\nProductos encontrados: {len(catalogo)}")

    # Validar que ningún producto tenga ya un ID
    productos_con_id = [
        producto for producto in catalogo
        if "id" in producto
    ]

    if productos_con_id:
        print(
            f"\nERROR: Se encontraron "
            f"{len(productos_con_id)} productos que ya tienen ID."
        )
        print("No se modificó el catálogo.")
        return

    # Agregar IDs consecutivos empezando desde 1
    for indice, producto in enumerate(catalogo, start=1):
        producto["id"] = indice

    # Guardar catálogo
    with open(CATALOGO, "w", encoding="utf-8") as f:
        json.dump(
            catalogo,
            f,
            ensure_ascii=False,
            indent=2
        )

    # Validaciones finales
    ids = [producto["id"] for producto in catalogo]

    ids_unicos = len(set(ids)) == len(ids)
    ids_correctos = ids == list(range(1, len(catalogo) + 1))

    print("\n========================================")
    print("             RESULTADO")
    print("========================================")
    print(f"Productos procesados : {len(catalogo)}")
    print(f"Primer ID            : {ids[0]}")
    print(f"Último ID            : {ids[-1]}")
    print(f"IDs únicos           : {'OK' if ids_unicos else 'ERROR'}")
    print(f"Secuencia correcta   : {'OK' if ids_correctos else 'ERROR'}")

    print("\nEjemplo:")
    print(json.dumps(catalogo[0], ensure_ascii=False, indent=2))

    print("\nProceso terminado correctamente.")


if __name__ == "__main__":
    main()