import { Link } from "react-router-dom";

import Header from "../components/Header";

import nosotrosHero from "../assets/nosotros-hero.jpg";
import nosotrosHistoria from "../assets/nosotros-historia.png";

function Icono({ tipo }) {
    if (tipo === "calidad") {
        return (
            <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="m12 3 2.2 4.45 4.9.71-3.55 3.46.84 4.88L12 14.2l-4.39 2.3.84-4.88L4.9 8.16l4.9-.71L12 3Z" />
            </svg>
        );
    }

    if (tipo === "confianza") {
        return (
            <svg viewBox="0 0 24 24" aria-hidden="true">
                <circle cx="9" cy="8" r="3" />
                <path d="M3.5 20c.4-3.2 2.3-5 5.5-5s5.1 1.8 5.5 5" />
                <circle cx="17" cy="9" r="2.3" />
                <path d="M16 14.8c2.6.1 4.2 1.7 4.5 4.2" />
            </svg>
        );
    }

    if (tipo === "estilo") {
        return (
            <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M19.5 4.5c-7.1.5-11.9 4-13.8 10.5" />
                <path d="M19.5 4.5c-.6 5.8-3.5 10-8.8 12.5" />
                <path d="M8.2 12.3c-1.8-.1-3.4.4-4.7 1.7" />
                <path d="M10.7 8.3c-.1-1.6.4-3 1.5-4.2" />
                <path d="M13.3 16.1c1.4.1 2.7-.3 3.8-1.2" />
            </svg>
        );
    }

    return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M12 20.5S4 15.8 4 9.5C4 6.8 6 5 8.5 5c1.6 0 2.8.8 3.5 2  .7-1.2 1.9-2 3.5-2C18 5 20 6.8 20 9.5c0 6.3-8 11-8 11Z" />
        </svg>
    );
}

function IconoServicio({ tipo }) {
    if (tipo === "envios") {
        return (
            <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M3 6h11v11H3z" />
                <path d="M14 9h4l3 3v5h-7" />
                <circle cx="7" cy="19" r="1.7" />
                <circle cx="18" cy="19" r="1.7" />
            </svg>
        );
    }

    if (tipo === "productos") {
        return (
            <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M12 3 20 6v6c0 4.5-3.1 7.6-8 9-4.9-1.4-8-4.5-8-9V6l8-3Z" />
            </svg>
        );
    }

    if (tipo === "atencion") {
        return (
            <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M5 13v-1a7 7 0 0 1 14 0v1" />
                <path d="M5 13H3.8A1.8 1.8 0 0 0 2 14.8v1.4A1.8 1.8 0 0 0 3.8 18H5v-5Z" />
                <path d="M19 13h1.2a1.8 1.8 0 0 1 1.8 1.8v1.4a1.8 1.8 0 0 1-1.8 1.8H19v-5Z" />
                <path d="M19 18c0 1.7-1.6 3-3.5 3H13" />
            </svg>
        );
    }

    return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
            <rect x="3" y="5" width="18" height="14" rx="1.5" />
            <path d="M3 10h18" />
            <path d="M7 15h4" />
        </svg>
    );
}

function Nosotros() {
    return (
        <>
            <Header />

            <main className="nosotros">

                {/* HERO */}

                <section className="nosotros-hero">

    <div
        className="nosotros-hero-imagen"
        style={{
            backgroundImage: `url(${nosotrosHero})`
        }}
    />

    <div className="nosotros-hero-overlay" />

                    <div className="nosotros-hero-contenedor">

                        <div className="nosotros-hero-card">

                            <span className="nosotros-eyebrow">
                                NOSOTROS
                            </span>

                            <span className="nosotros-linea" />

                            <h1>
                                Más que accesorios,
                                <br />
                                conectamos personas
                                <br />
                                con su esencia.
                            </h1>

                            <p>
                                En TuEsencia somos una empresa
                                dedicada a la distribución de
                                accesorios y productos de catálogo.
                                Seleccionamos referencias que
                                combinan estilo, variedad y calidad,
                                acercándolas a nuestros clientes de
                                una manera sencilla y confiable.
                            </p>

                            <div className="nosotros-hero-caracteristicas">

                                <div>
                                    <span className="nosotros-hero-icono">
                                        <Icono tipo="calidad" />
                                    </span>

                                    <span>
                                        Productos
                                        <br />
                                        seleccionados
                                    </span>
                                </div>

                                <div>
                                    <span className="nosotros-hero-icono">
                                        <IconoServicio tipo="envios" />
                                    </span>

                                    <span>
                                        Distribución
                                        <br />
                                        confiable
                                    </span>
                                </div>

                                <div>
                                    <span className="nosotros-hero-icono">
                                        <Icono tipo="personas" />
                                    </span>

                                    <span>
                                        Tu estilo,
                                        <br />
                                        nuestra inspiración
                                    </span>
                                </div>

                            </div>

                        </div>

                    </div>

                </section>


                {/* HISTORIA */}

                <section className="nosotros-historia">

                    <div className="nosotros-seccion-encabezado">

                        <span className="nosotros-eyebrow">
                            NUESTRA HISTORIA
                        </span>

                        <span className="nosotros-linea" />

                        <h2>
                            Una propuesta que sigue creciendo
                        </h2>

                    </div>

                    <div className="nosotros-historia-contenedor">

                        <div className="nosotros-historia-imagen">
                            <img
                                src={nosotrosHistoria}
                                alt="Accesorios TuEsencia"
                                loading="lazy"
                            />
                        </div>

                        <div className="nosotros-historia-texto">

                            <p>
                                TuEsencia nace con la idea de
                                acercar productos de catálogo a
                                más personas, reuniendo diferentes
                                estilos y opciones en un solo lugar.
                            </p>

                            <p>
                                Nuestra propuesta se basa en
                                ofrecer una experiencia sencilla
                                para descubrir productos, conocer
                                sus características y encontrar
                                aquellos que conectan con cada
                                persona.
                            </p>

                            <p>
                                Seguimos creciendo con una idea
                                clara: que cada elección tenga
                                algo de tu esencia.
                            </p>

                            <Link
                                to="/"
                                className="nosotros-boton"
                            >
                                Conoce nuestro catálogo
                                <span aria-hidden="true">
                                    →
                                </span>
                            </Link>

                        </div>

                    </div>

                </section>


                {/* VALORES */}

                <section className="nosotros-valores">

                    <div className="nosotros-seccion-encabezado">

                        <span className="nosotros-eyebrow">
                            NUESTROS VALORES
                        </span>

                        <span className="nosotros-linea" />

                        <h2>
                            Lo que nos impulsa cada día
                        </h2>

                    </div>

                    <div className="nosotros-valores-grid">

                        <article className="nosotros-valor">

                            <div className="nosotros-valor-icono">
                                <Icono tipo="calidad" />
                            </div>

                            <h3>
                                Calidad
                            </h3>

                            <p>
                                Seleccionamos productos
                                pensando en ofrecer una
                                experiencia satisfactoria.
                            </p>

                        </article>

                        <article className="nosotros-valor">

                            <div className="nosotros-valor-icono">
                                <Icono tipo="confianza" />
                            </div>

                            <h3>
                                Confianza
                            </h3>

                            <p>
                                Construimos relaciones
                                basadas en transparencia
                                y cumplimiento.
                            </p>

                        </article>

                        <article className="nosotros-valor">

                            <div className="nosotros-valor-icono">
                                <Icono tipo="estilo" />
                            </div>

                            <h3>
                                Estilo
                            </h3>

                            <p>
                                Una colección diversa para
                                diferentes gustos y
                                personalidades.
                            </p>

                        </article>

                        <article className="nosotros-valor">

                            <div className="nosotros-valor-icono">
                                <Icono tipo="personas" />
                            </div>

                            <h3>
                                Personas
                            </h3>

                            <p>
                                Porque detrás de cada elección
                                hay una persona, una historia
                                y una esencia.
                            </p>

                        </article>

                    </div>

                </section>


                {/* CTA */}

                <section className="nosotros-cta">

    <div
        className="nosotros-cta-imagen"
        style={{
            backgroundImage: `url(${nosotrosHero})`
        }}
    />

                    <div className="nosotros-cta-overlay" />

                    <div className="nosotros-cta-contenido">

                        <span className="nosotros-eyebrow">
                            TU ESENCIA TAMBIÉN CUENTA
                        </span>

                        <h2>
                            Descubre nuestra colección
                        </h2>

                        <p>
                            Explora accesorios que se adaptan
                            a tu estilo, a tu día y a tu historia.
                        </p>

                        <Link
                            to="/"
                            className="nosotros-cta-boton"
                        >
                            Explorar catálogo
                            <span aria-hidden="true">
                                →
                            </span>
                        </Link>

                    </div>

                </section>


                {/* SERVICIOS */}

                <section className="nosotros-servicios">

                    <div className="nosotros-servicio">

                        <div className="nosotros-servicio-icono">
                            <IconoServicio tipo="envios" />
                        </div>

                        <h3>
                            Envíos confiables
                        </h3>

                        <p>
                            A todo el país
                        </p>

                    </div>

                    <div className="nosotros-servicio">

                        <div className="nosotros-servicio-icono">
                            <IconoServicio tipo="productos" />
                        </div>

                        <h3>
                            Productos seleccionados
                        </h3>

                        <p>
                            Variedad para cada estilo
                        </p>

                    </div>

                    <div className="nosotros-servicio">

                        <div className="nosotros-servicio-icono">
                            <IconoServicio tipo="atencion" />
                        </div>

                        <h3>
                            Atención personalizada
                        </h3>

                        <p>
                            Estamos para ayudarte
                        </p>

                    </div>

                    <div className="nosotros-servicio">

                        <div className="nosotros-servicio-icono">
                            <IconoServicio tipo="pagos" />
                        </div>

                        <h3>
                            Pagos seguros
                        </h3>

                        <p>
                            Compra con tranquilidad
                        </p>

                    </div>

                </section>

            </main>
        </>
    );
}

export default Nosotros;