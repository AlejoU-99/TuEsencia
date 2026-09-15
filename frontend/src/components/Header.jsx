import { useEffect, useState } from "react";
import {
    Link,
    useSearchParams
} from "react-router-dom";

import logoHeader from "../assets/header.png";


function Header({ busqueda, onBuscar }) {

    const [searchParams] =
        useSearchParams();


    const [buscadorAbierto, setBuscadorAbierto] =
        useState(false);

    const [menuAbierto, setMenuAbierto] =
        useState(false);


    /*
     * Si el Header está en una página que no recibe
     * directamente la búsqueda, la recuperamos desde
     * la URL.
     */

    const busquedaUrl =
        searchParams.get("busqueda") || "";


    const busquedaActual =
        busqueda !== undefined
            ? busqueda
            : busquedaUrl;


    const [textoBusqueda, setTextoBusqueda] =
        useState(busquedaActual);


    /*
     * Mantener sincronizado el texto del buscador
     * cuando cambia la búsqueda.
     */

    useEffect(() => {

        setTextoBusqueda(
            busquedaActual
        );

    }, [busquedaActual]);


    /*
     * Bloquear scroll cuando el menú móvil
     * está abierto.
     */

    useEffect(() => {

        if (menuAbierto) {

            document.body.style.overflow =
                "hidden";

        } else {

            document.body.style.overflow =
                "";

        }


        return () => {

            document.body.style.overflow =
                "";

        };

    }, [menuAbierto]);


    /*
     * Cerrar menú y buscador con Escape.
     */

    useEffect(() => {

        function manejarTecla(event) {

            if (event.key === "Escape") {

                setMenuAbierto(false);

                setBuscadorAbierto(false);

            }

        }


        document.addEventListener(
            "keydown",
            manejarTecla
        );


        return () => {

            document.removeEventListener(
                "keydown",
                manejarTecla
            );

        };

    }, []);


    /*
     * Realizar búsqueda.
     */

    function manejarSubmit(event) {

        event.preventDefault();


        onBuscar(
            textoBusqueda.trim()
        );


        setBuscadorAbierto(false);

        setMenuAbierto(false);

    }


    /*
     * Limpiar búsqueda.
     */

    function limpiarBusqueda() {

        setTextoBusqueda("");

        onBuscar("");

    }


    /*
     * Abrir buscador.
     */

    function abrirBuscador() {

        setBuscadorAbierto(true);

        setMenuAbierto(false);

    }


    /*
     * Cerrar buscador.
     */

    function cerrarBuscador() {

        setBuscadorAbierto(false);

    }


    /*
     * Abrir / cerrar menú móvil.
     */

    function alternarMenu() {

        setMenuAbierto(
            (estado) => !estado
        );

        setBuscadorAbierto(false);

    }


    /*
     * Cerrar menú móvil.
     */

    function cerrarMenu() {

        setMenuAbierto(false);

    }


    return (
        <>

            <header className="site-header">

                <div className="header-container">


                    {/* =====================================
                        LOGO
                    ===================================== */}

                    <Link
                        to="/"
                        className="brand"
                        onClick={cerrarMenu}
                        aria-label="TuEsencia - Inicio"
                    >

                        <img
                            src={logoHeader}
                            alt="TuEsencia"
                            className="brand-logo"
                        />

                    </Link>


                    {/* =====================================
                        NAVEGACIÓN DESKTOP
                    ===================================== */}

                    <nav className="main-navigation">

                        <Link
                            to="/"
                            className="nav-link active"
                        >
                            Catálogo
                        </Link>


                        <Link
                            to="/nosotros"
                            className="nav-link"
                        >
                            Nosotros
                        </Link>

                    </nav>


                    {/* =====================================
                        ACCIONES
                    ===================================== */}

                    <div className="header-actions">


                        {/* =================================
                            BUSCADOR DESKTOP
                        ================================= */}

                        {!buscadorAbierto && (

                            <button
                                type="button"
                                className="header-action desktop-search-button"
                                aria-label="Buscar productos"
                                onClick={abrirBuscador}
                            >

                                <svg
                                    viewBox="0 0 24 24"
                                    aria-hidden="true"
                                >

                                    <circle
                                        cx="11"
                                        cy="11"
                                        r="6.5"
                                    />

                                    <path d="m16 16 5 5" />

                                </svg>

                            </button>

                        )}


                        {buscadorAbierto && (

                            <form
                                className="header-search"
                                onSubmit={manejarSubmit}
                            >

                                <svg
                                    viewBox="0 0 24 24"
                                    aria-hidden="true"
                                >

                                    <circle
                                        cx="11"
                                        cy="11"
                                        r="6.5"
                                    />

                                    <path d="m16 16 5 5" />

                                </svg>


                                <input
                                    type="search"
                                    placeholder="Buscar productos..."
                                    value={textoBusqueda}
                                    onChange={(event) =>
                                        setTextoBusqueda(
                                            event.target.value
                                        )
                                    }
                                    autoFocus
                                    aria-label="Buscar productos"
                                />


                                {textoBusqueda && (

                                    <button
                                        type="button"
                                        className="header-search-clear"
                                        aria-label="Limpiar búsqueda"
                                        onClick={limpiarBusqueda}
                                    >
                                        ×
                                    </button>

                                )}


                                <button
                                    type="button"
                                    className="header-search-close"
                                    aria-label="Cerrar búsqueda"
                                    onClick={cerrarBuscador}
                                >
                                    ×
                                </button>

                            </form>

                        )}


                        {/* =================================
                            MENÚ MÓVIL
                        ================================= */}

                        <button
                            type="button"
                            className="header-action mobile-menu"
                            aria-label={
                                menuAbierto
                                    ? "Cerrar menú"
                                    : "Abrir menú"
                            }
                            aria-expanded={menuAbierto}
                            onClick={alternarMenu}
                        >

                            {menuAbierto ? (

                                <svg
                                    viewBox="0 0 24 24"
                                    aria-hidden="true"
                                >

                                    <path d="M5 5l14 14" />

                                    <path d="M19 5L5 19" />

                                </svg>

                            ) : (

                                <svg
                                    viewBox="0 0 24 24"
                                    aria-hidden="true"
                                >

                                    <path d="M4 7h16" />

                                    <path d="M4 12h16" />

                                    <path d="M4 17h16" />

                                </svg>

                            )}

                        </button>

                    </div>

                </div>

            </header>


            {/* =========================================
                OVERLAY
            ========================================= */}

            <div
                className={`mobile-overlay ${
                    menuAbierto
                        ? "visible"
                        : ""
                }`}
                onClick={cerrarMenu}
                aria-hidden="true"
            />


            {/* =========================================
                MENÚ MÓVIL
            ========================================= */}

            <aside
                className={`mobile-navigation ${
                    menuAbierto
                        ? "open"
                        : ""
                }`}
                aria-hidden={!menuAbierto}
            >

                <div className="mobile-navigation-header">

                    <span className="mobile-navigation-title">
                        Menú
                    </span>


                    <button
                        type="button"
                        className="mobile-navigation-close"
                        onClick={cerrarMenu}
                        aria-label="Cerrar menú"
                    >
                        ×
                    </button>

                </div>


                <nav className="mobile-navigation-links">

                    <Link
                        to="/"
                        onClick={cerrarMenu}
                    >
                        Catálogo
                    </Link>


                    <Link
    to="/nosotros"
    onClick={cerrarMenu}
>
    Nosotros
</Link>

                </nav>


                {/* =====================================
                    BUSCADOR MÓVIL
                ===================================== */}

                <form
                    className="mobile-search"
                    onSubmit={manejarSubmit}
                >

                    <label htmlFor="mobile-search-input">
                        Buscar
                    </label>


                    <div className="mobile-search-input">

                        <svg
                            viewBox="0 0 24 24"
                            aria-hidden="true"
                        >

                            <circle
                                cx="11"
                                cy="11"
                                r="6.5"
                            />

                            <path d="m16 16 5 5" />

                        </svg>


                        <input
                            id="mobile-search-input"
                            type="search"
                            placeholder="Buscar productos..."
                            value={textoBusqueda}
                            onChange={(event) =>
                                setTextoBusqueda(
                                    event.target.value
                                )
                            }
                        />


                        {textoBusqueda && (

                            <button
                                type="button"
                                className="mobile-search-clear"
                                aria-label="Limpiar búsqueda"
                                onClick={limpiarBusqueda}
                            >
                                ×
                            </button>

                        )}

                    </div>

                </form>


                <div className="mobile-navigation-footer">

                    <span>
                        TuEsencia
                    </span>

                    <span>
                        MÁS QUE ACCESORIOS, ES PARTE DE TI
                    </span>

                </div>

            </aside>

        </>
    );
}


export default Header;