import { useEffect, useState } from "react";
import {
    useSearchParams
} from "react-router-dom";

import Header from "../components/Header";
import Filtros from "../components/Filtros";
import GridProductos from "../components/GridProductos";
import Paginacion from "../components/Paginacion";

import {
    obtenerProductos,
    obtenerOpcionesFiltros
} from "../services/api";


function Catalogo() {

    const [searchParams, setSearchParams] =
        useSearchParams();


    /* =========================================
       ESTADO INICIAL DESDE LA URL
    ========================================= */

    const paginaInicial =
        Number(searchParams.get("pagina")) || 1;

    const busquedaInicial =
        searchParams.get("busqueda") || "";

    const filtrosIniciales = {
        categoria:
            searchParams.get("categoria") || "",

        tipo:
            searchParams.get("tipo") || "",

        color:
            searchParams.get("color") || "",

        estilo:
            searchParams.get("estilo") || "",

        material:
            searchParams.get("material") || "",

        precio_min:
            searchParams.get("precio_min") || "",

        precio_max:
            searchParams.get("precio_max") || ""
    };

    const ordenInicial =
        searchParams.get("orden") || "default";


    /* =========================================
       PRODUCTOS
    ========================================= */

    const [productos, setProductos] =
        useState([]);


    /* =========================================
       OPCIONES DINÁMICAS
    ========================================= */

    const [opciones, setOpciones] =
        useState(null);


    /* =========================================
       PAGINACIÓN
    ========================================= */

    const [totalProductos, setTotalProductos] =
        useState(0);

    const [totalPaginas, setTotalPaginas] =
        useState(1);

    const [pagina, setPagina] =
        useState(paginaInicial);


    /* =========================================
       BÚSQUEDA
    ========================================= */

    const [busqueda, setBusqueda] =
        useState(busquedaInicial);


    /* =========================================
       FILTROS
    ========================================= */

    const [filtros, setFiltros] =
        useState(filtrosIniciales);


    /* =========================================
       ORDEN
    ========================================= */

    const [orden, setOrden] =
        useState(ordenInicial);


    /* =========================================
       ESTADOS
    ========================================= */

    const [cargando, setCargando] =
        useState(true);

    const [cargandoOpciones, setCargandoOpciones] =
        useState(true);

    const [error, setError] =
        useState(null);


    /* =========================================
       SINCRONIZAR ESTADO → URL
    ========================================= */

    useEffect(() => {

        const nuevosParametros = {};


        if (pagina > 1) {
            nuevosParametros.pagina = pagina;
        }


        if (busqueda) {
            nuevosParametros.busqueda = busqueda;
        }


        if (filtros.categoria) {
            nuevosParametros.categoria =
                filtros.categoria;
        }


        if (filtros.tipo) {
            nuevosParametros.tipo =
                filtros.tipo;
        }


        if (filtros.color) {
            nuevosParametros.color =
                filtros.color;
        }


        if (filtros.estilo) {
            nuevosParametros.estilo =
                filtros.estilo;
        }


        if (filtros.material) {
            nuevosParametros.material =
                filtros.material;
        }


        if (filtros.precio_min) {
            nuevosParametros.precio_min =
                filtros.precio_min;
        }


        if (filtros.precio_max) {
            nuevosParametros.precio_max =
                filtros.precio_max;
        }


        if (orden !== "default") {
            nuevosParametros.orden =
                orden;
        }


        setSearchParams(
            nuevosParametros,
            {
                replace: true
            }
        );

    }, [
        pagina,
        busqueda,
        filtros,
        orden,
        setSearchParams
    ]);


    /* =========================================
       CARGAR PRODUCTOS
    ========================================= */

    useEffect(() => {

        async function cargarProductos() {

            setCargando(true);

            setError(null);


            try {

                const datos =
                    await obtenerProductos({

                        pagina: pagina,

                        limite: 24,

                        busqueda: busqueda,

                        categoria:
                            filtros.categoria,

                        tipo:
                            filtros.tipo,

                        color:
                            filtros.color,

                        estilo:
                            filtros.estilo,

                        material:
                            filtros.material,

                        precio_min:
                            filtros.precio_min,

                        precio_max:
                            filtros.precio_max,

                        orden:
                            orden

                    });


                setProductos(
                    datos.productos
                );


                setTotalProductos(
                    datos.total
                );


                setTotalPaginas(
                    datos.total_paginas
                );


            } catch (err) {

                setError(
                    err.message
                );

            } finally {

                setCargando(false);

            }

        }


        cargarProductos();

    }, [
        pagina,
        busqueda,
        filtros,
        orden
    ]);


    /* =========================================
       CARGAR OPCIONES DINÁMICAS
    ========================================= */

    useEffect(() => {

        async function cargarOpciones() {

            setCargandoOpciones(true);


            try {

                const datos =
                    await obtenerOpcionesFiltros({

                        busqueda:
                            busqueda,

                        categoria:
                            filtros.categoria,

                        tipo:
                            filtros.tipo,

                        color:
                            filtros.color,

                        estilo:
                            filtros.estilo,

                        material:
                            filtros.material,

                        precio_min:
                            filtros.precio_min,

                        precio_max:
                            filtros.precio_max

                    });


                setOpciones(
                    datos
                );


            } catch (err) {

                setError(
                    err.message
                );

            } finally {

                setCargandoOpciones(false);

            }

        }


        cargarOpciones();

    }, [
        busqueda,
        filtros
    ]);


    /* =========================================
       BÚSQUEDA
    ========================================= */

    function realizarBusqueda(texto) {

        setBusqueda(
            texto.trim()
        );

        setPagina(1);

    }


    /* =========================================
       CAMBIAR FILTRO
    ========================================= */

    function cambiarFiltro(
        nombre,
        valor
    ) {

        setFiltros(
            (filtrosActuales) => ({

                ...filtrosActuales,

                [nombre]: valor

            })
        );


        setPagina(1);

    }


    /* =========================================
       LIMPIAR FILTROS
    ========================================= */

    function limpiarFiltros() {

        setFiltros({

            categoria: "",

            tipo: "",

            color: "",

            estilo: "",

            material: "",

            precio_min: "",

            precio_max: ""

        });


        setPagina(1);

    }


    /* =========================================
       FILTROS ACTIVOS
    ========================================= */

    const filtrosActivos = [];


    if (filtros.categoria) {

        filtrosActivos.push({

            clave: "categoria",

            etiqueta: "Categoría",

            valor: filtros.categoria

        });

    }


    if (filtros.tipo) {

        filtrosActivos.push({

            clave: "tipo",

            etiqueta: "Tipo",

            valor: filtros.tipo

        });

    }


    if (filtros.color) {

        filtrosActivos.push({

            clave: "color",

            etiqueta: "Color",

            valor: filtros.color

        });

    }


    if (filtros.estilo) {

        filtrosActivos.push({

            clave: "estilo",

            etiqueta: "Estilo",

            valor: filtros.estilo

        });

    }


    if (filtros.material) {

        filtrosActivos.push({

            clave: "material",

            etiqueta: "Material",

            valor: filtros.material

        });

    }


    if (filtros.precio_min) {

        filtrosActivos.push({

            clave: "precio_min",

            etiqueta: "Desde",

            valor:
                `$${Number(
                    filtros.precio_min
                ).toLocaleString("es-CO")}`

        });

    }


    if (filtros.precio_max) {

        filtrosActivos.push({

            clave: "precio_max",

            etiqueta: "Hasta",

            valor:
                `$${Number(
                    filtros.precio_max
                ).toLocaleString("es-CO")}`

        });

    }


    const hayFiltrosActivos =
        filtrosActivos.length > 0 ||
        Boolean(busqueda);


    /* =========================================
       RANGO DE RESULTADOS
    ========================================= */

    const limitePorPagina = 24;


    const primerResultado =
        totalProductos === 0

            ? 0

            : ((pagina - 1) *
                limitePorPagina) + 1;


    const ultimoResultado =
        totalProductos === 0

            ? 0

            : Math.min(
                pagina *
                limitePorPagina,
                totalProductos
            );


    /* =========================================
       ERROR
    ========================================= */

    if (error) {

        return (
            <>

                <Header
                    busqueda={busqueda}
                    onBuscar={realizarBusqueda}
                />


                <main className="catalogo">

                    <div className="catalogo-error">

                        <h2>
                            No pudimos cargar el catálogo
                        </h2>

                        <p>
                            {error}
                        </p>

                    </div>

                </main>

            </>
        );

    }


    return (
        <>

            <Header
                busqueda={busqueda}
                onBuscar={realizarBusqueda}
            />


            <main className="catalogo">


                {/* =====================================
                    INTRO
                ===================================== */}

                <section className="catalogo-intro">

                    <span className="catalogo-eyebrow">
                        COLECCIÓN
                    </span>


                    <h1>

                        Encuentra algo que

                        <br />

                        hable de ti.

                    </h1>


                    <p>

                        Explora nuestra colección de accesorios
                        y encuentra tu próxima pieza favorita.

                    </p>

                </section>


                {/* =====================================
                    PRODUCTOS
                ===================================== */}

                <section className="catalogo-productos">


                    {/* =================================
                        TOOLBAR
                    ================================= */}

                    <div className="catalogo-toolbar">

                        <div className="catalogo-resultados">

                            <span className="catalogo-contador">

                                {totalProductos.toLocaleString(
                                    "es-CO"
                                )}

                                {" "}

                                {totalProductos === 1
                                    ? "producto"
                                    : "productos"}

                            </span>


                            {!cargando &&
                                totalProductos > 0 && (

                                    <span className="catalogo-rango">

                                        Mostrando{" "}

                                        {primerResultado.toLocaleString(
                                            "es-CO"
                                        )}

                                        {"–"}

                                        {ultimoResultado.toLocaleString(
                                            "es-CO"
                                        )}

                                    </span>

                                )}

                        </div>


                        <div className="catalogo-orden">

                            <span>
                                Ordenar por
                            </span>


                            <select
                                value={orden}
                                onChange={(e) => {

                                    setOrden(
                                        e.target.value
                                    );

                                    setPagina(1);

                                }}
                            >

                                <option value="default">
                                    Más relevantes
                                </option>

                                <option value="precio_asc">
                                    Precio: menor a mayor
                                </option>

                                <option value="precio_desc">
                                    Precio: mayor a menor
                                </option>

                                <option value="nombre_asc">
                                    Nombre: A-Z
                                </option>

                                <option value="nombre_desc">
                                    Nombre: Z-A
                                </option>

                            </select>

                        </div>

                    </div>


                    {/* =================================
                        BÚSQUEDA ACTIVA
                    ================================= */}

                    {busqueda && (

                        <div className="busqueda-activa">

                            <span>
                                Resultados para:
                            </span>


                            <strong>
                                "{busqueda}"
                            </strong>


                            <button
                                type="button"
                                onClick={() =>
                                    realizarBusqueda("")
                                }
                                aria-label="Limpiar búsqueda"
                            >
                                ×
                            </button>

                        </div>

                    )}


                    {/* =================================
                        FILTROS
                    ================================= */}

                    {cargandoOpciones ? (

                        <div className="filtros-cargando">

                            Actualizando filtros...

                        </div>

                    ) : (

                        <Filtros

                            opciones={opciones}

                            filtros={filtros}

                            onCambioFiltro={
                                cambiarFiltro
                            }

                            onLimpiarFiltros={
                                limpiarFiltros
                            }

                        />

                    )}


                    {/* =================================
                        FILTROS ACTIVOS
                    ================================= */}

                    {hayFiltrosActivos && (

                        <div className="filtros-activos">

                            <span className="filtros-activos-label">

                                Filtros activos

                            </span>


                            <div className="filtros-activos-lista">


                                {busqueda && (

                                    <button
                                        type="button"
                                        className="filtro-chip"
                                        onClick={() =>
                                            realizarBusqueda("")
                                        }
                                    >

                                        <span>

                                            Búsqueda:{" "}

                                            <strong>
                                                {busqueda}
                                            </strong>

                                        </span>


                                        <span
                                            className="filtro-chip-cerrar"
                                            aria-hidden="true"
                                        >
                                            ×
                                        </span>

                                    </button>

                                )}


                                {filtrosActivos.map(
                                    (filtro) => (

                                        <button
                                            key={
                                                filtro.clave
                                            }
                                            type="button"
                                            className="filtro-chip"
                                            onClick={() =>
                                                cambiarFiltro(
                                                    filtro.clave,
                                                    ""
                                                )
                                            }
                                        >

                                            <span>

                                                {filtro.etiqueta}

                                                {": "}

                                                <strong>
                                                    {filtro.valor}
                                                </strong>

                                            </span>


                                            <span
                                                className="filtro-chip-cerrar"
                                                aria-hidden="true"
                                            >
                                                ×
                                            </span>

                                        </button>

                                    )
                                )}

                            </div>

                        </div>

                    )}


                    {/* =================================
                        PRODUCTOS
                    ================================= */}

                    {cargando ? (

                        <div className="catalogo-cargando">

                            Cargando productos...

                        </div>

                    ) : productos.length === 0 ? (

                        <div className="catalogo-vacio">

                            <h2>
                                No encontramos productos
                            </h2>


                            <p>

                                Prueba cambiando los filtros
                                o realizando otra búsqueda.

                            </p>


                            <button
                                type="button"
                                onClick={() => {

                                    realizarBusqueda("");

                                    limpiarFiltros();

                                }}
                            >

                                Limpiar búsqueda y filtros

                            </button>

                        </div>


                    ) : (

                        <>

                            <GridProductos
                                productos={productos}
                            />


                            <Paginacion

                                pagina={pagina}

                                totalPaginas={
                                    totalPaginas
                                }

                                onCambiarPagina={
                                    setPagina
                                }

                            />

                        </>

                    )}

                </section>

            </main>

        </>
    );
}


export default Catalogo;