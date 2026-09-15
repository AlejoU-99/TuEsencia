const CATALOGO_URL = "/catalogo.json";

let catalogoCache = null;


/* =========================================================
   CARGAR CATÁLOGO
   ========================================================= */

async function cargarCatalogo() {

    if (catalogoCache) {
        return catalogoCache;
    }

    const respuesta = await fetch(CATALOGO_URL);

    if (!respuesta.ok) {
        throw new Error(
            "No pudimos cargar el catálogo."
        );
    }

    catalogoCache = await respuesta.json();

    return catalogoCache;
}


/* =========================================================
   UTILIDADES
   ========================================================= */

function obtenerValorFaceta(
    producto,
    faceta
) {
    if (faceta === "categoria") {
        return producto.categoria;
    }

    return producto.atributos?.[faceta] || null;
}


function productoCoincide(
    producto,
    filtros
) {
    const {
        busqueda,
        categoria,
        tipo,
        color,
        estilo,
        material,
        precio_min,
        precio_max
    } = filtros;


    /* -------------------------
       Búsqueda
       ------------------------- */

    if (busqueda) {

        const texto =
            busqueda
                .toLowerCase()
                .trim();

        const coincideBusqueda =
            producto.nombre
                ?.toLowerCase()
                .includes(texto) ||

            producto.slug
                ?.toLowerCase()
                .includes(texto) ||

            producto.sku
                ?.toLowerCase()
                .includes(texto);

        if (!coincideBusqueda) {
            return false;
        }
    }


    /* -------------------------
       Categoría
       ------------------------- */

    if (
        categoria &&
        producto.categoria !== categoria
    ) {
        return false;
    }


    /* -------------------------
       Atributos
       ------------------------- */

    const filtrosAtributos = {
        tipo,
        color,
        estilo,
        material
    };

    for (
        const [faceta, valor]
        of Object.entries(filtrosAtributos)
    ) {

        if (
            valor &&
            producto.atributos?.[faceta] !== valor
        ) {
            return false;
        }
    }


    /* -------------------------
       Precio mínimo
       ------------------------- */

    if (
        precio_min !== undefined &&
        precio_min !== null &&
        precio_min !== ""
    ) {

        if (
            producto.precio_venta <
            Number(precio_min)
        ) {
            return false;
        }
    }


    /* -------------------------
       Precio máximo
       ------------------------- */

    if (
        precio_max !== undefined &&
        precio_max !== null &&
        precio_max !== ""
    ) {

        if (
            producto.precio_venta >
            Number(precio_max)
        ) {
            return false;
        }
    }


    return true;
}


/* =========================================================
   FILTRAR
   ========================================================= */

function filtrarProductos(
    productos,
    filtros
) {
    return productos.filter(
        (producto) =>
            productoCoincide(
                producto,
                filtros
            )
    );
}


/* =========================================================
   ORDENAR
   ========================================================= */

function ordenarProductos(
    productos,
    orden
) {

    const resultado = [
        ...productos
    ];

    switch (orden) {

        case "precio_asc":

            resultado.sort(
                (a, b) =>
                    a.precio_venta -
                    b.precio_venta
            );

            break;


        case "precio_desc":

            resultado.sort(
                (a, b) =>
                    b.precio_venta -
                    a.precio_venta
            );

            break;


        case "nombre_asc":

            resultado.sort(
                (a, b) =>
                    a.nombre.localeCompare(
                        b.nombre,
                        "es",
                        {
                            sensitivity: "base"
                        }
                    )
            );

            break;


        case "nombre_desc":

            resultado.sort(
                (a, b) =>
                    b.nombre.localeCompare(
                        a.nombre,
                        "es",
                        {
                            sensitivity: "base"
                        }
                    )
            );

            break;


        default:
            /*
             * Se conserva el orden original
             * del catalogo.json.
             */
            break;
    }

    return resultado;
}


/* =========================================================
   OBTENER PRODUCTOS
   ========================================================= */

export async function obtenerProductos(
    params = {}
) {

    const productos =
        await cargarCatalogo();


    const filtros = {

        busqueda:
            params.busqueda || "",

        categoria:
            params.categoria || "",

        tipo:
            params.tipo || "",

        color:
            params.color || "",

        estilo:
            params.estilo || "",

        material:
            params.material || "",

        precio_min:
            params.precio_min || "",

        precio_max:
            params.precio_max || ""
    };


    let resultados =
        filtrarProductos(
            productos,
            filtros
        );


    resultados =
        ordenarProductos(
            resultados,
            params.orden || "default"
        );


    /* -------------------------
       Paginación
       ------------------------- */

    const pagina =
        Math.max(
            1,
            Number(params.pagina) || 1
        );

    const limite =
        Math.min(
            100,
            Math.max(
                1,
                Number(params.limite) || 24
            )
        );

    const total =
        resultados.length;

    const totalPaginas =
        Math.max(
            1,
            Math.ceil(
                total / limite
            )
        );


    /*
     * Si la página solicitada
     * supera el total, usamos
     * la última página disponible.
     */

    const paginaReal =
        Math.min(
            pagina,
            totalPaginas
        );


    const inicio =
        (paginaReal - 1) *
        limite;

    const fin =
        inicio + limite;


    const productosPagina =
        resultados.slice(
            inicio,
            fin
        );


    return {

        productos:
            productosPagina,

        total,

        pagina:
            paginaReal,

        limite,

        total_paginas:
            totalPaginas
    };
}


/* =========================================================
   OBTENER PRODUCTO
   ========================================================= */

export async function obtenerProducto(
    id
) {

    const productos =
        await cargarCatalogo();


    const producto =
        productos.find(
            (item) =>
                Number(item.id) ===
                Number(id)
        );


    if (!producto) {
        throw new Error(
            "Producto no encontrado"
        );
    }


    return producto;
}


/* =========================================================
   CATEGORÍAS
   ========================================================= */

export async function obtenerCategorias() {

    const productos =
        await cargarCatalogo();


    const valores =
        new Set();


    productos.forEach(
        (producto) => {

            if (producto.categoria) {
                valores.add(
                    producto.categoria
                );
            }

        }
    );


    return [
        ...valores
    ].sort(
        (a, b) =>
            a.localeCompare(
                b,
                "es",
                {
                    sensitivity: "base"
                }
            )
    );
}


/* =========================================================
   ATRIBUTOS
   ========================================================= */

export async function obtenerAtributos() {

    const productos =
        await cargarCatalogo();


    const resultado = {

        tipo: new Set(),

        color: new Set(),

        estilo: new Set(),

        material: new Set()
    };


    productos.forEach(
        (producto) => {

            Object.keys(
                resultado
            ).forEach(
                (faceta) => {

                    const valor =
                        producto
                            .atributos?.[
                                faceta
                            ];

                    if (valor) {
                        resultado[
                            faceta
                        ].add(valor);
                    }

                }
            );

        }
    );


    return {

        tipo: [
            ...resultado.tipo
        ].sort(),

        color: [
            ...resultado.color
        ].sort(),

        estilo: [
            ...resultado.estilo
        ].sort(),

        material: [
            ...resultado.material
        ].sort()
    };
}


/* =========================================================
   OPCIONES DINÁMICAS DE FILTROS
   ========================================================= */

export async function obtenerOpcionesFiltros(
    params = {}
) {

    const productos =
        await cargarCatalogo();


    const FACETAS = [
        "categoria",
        "tipo",
        "color",
        "estilo",
        "material"
    ];


    const filtros = {

        busqueda:
            params.busqueda || "",

        categoria:
            params.categoria || "",

        tipo:
            params.tipo || "",

        color:
            params.color || "",

        estilo:
            params.estilo || "",

        material:
            params.material || "",

        precio_min:
            params.precio_min || "",

        precio_max:
            params.precio_max || ""
    };


    const resultado = {};


    FACETAS.forEach(
        (faceta) => {

            /*
             * Para calcular las opciones
             * de una faceta excluimos
             * solamente su propio filtro.
             *
             * Los demás filtros sí se mantienen.
             */

            const filtrosSinFaceta = {
                ...filtros,
                [faceta]: ""
            };


            const productosFiltrados =
                filtrarProductos(
                    productos,
                    filtrosSinFaceta
                );


            const conteos =
                new Map();


            productosFiltrados.forEach(
                (producto) => {

                    const valor =
                        obtenerValorFaceta(
                            producto,
                            faceta
                        );

                    if (!valor) {
                        return;
                    }


                    conteos.set(
                        valor,
                        (
                            conteos.get(
                                valor
                            ) || 0
                        ) + 1
                    );

                }
            );


            /*
             * Si existe un filtro seleccionado
             * pero actualmente no aparece
             * entre los resultados, lo
             * conservamos con total 0.
             */

            const valorSeleccionado =
                filtros[faceta];


            if (
                valorSeleccionado &&
                !conteos.has(
                    valorSeleccionado
                )
            ) {
                conteos.set(
                    valorSeleccionado,
                    0
                );
            }


            resultado[faceta] =
                [
                    ...conteos.entries()
                ]
                .map(
                    (
                        [valor, total]
                    ) => ({
                        valor,
                        total
                    })
                )
                .sort(
                    (a, b) =>
                        a.valor.localeCompare(
                            b.valor,
                            "es",
                            {
                                sensitivity:
                                    "base"
                            }
                        )
                );

        }
    );


    return resultado;
}