import { useEffect, useState } from "react";
import {
    useParams,
    Link,
    useSearchParams
} from "react-router-dom";

import Header from "../components/Header";
import { obtenerProducto } from "../services/api";

import logo from "../assets/logo.png";

function ProductoDetalle() {
    const { id } = useParams();

    const [searchParams] = useSearchParams();

    const [producto, setProducto] = useState(null);
    const [cargando, setCargando] = useState(true);
    const [error, setError] = useState(null);

    const parametrosCatalogo =
        searchParams.toString();

    const urlCatalogo =
        parametrosCatalogo
            ? `/?${parametrosCatalogo}`
            : "/";

    useEffect(() => {
        async function cargarProducto() {
            setCargando(true);
            setError(null);

            try {
                const datos =
                    await obtenerProducto(id);

                setProducto(datos);
            } catch (err) {
                setError(err.message);
            } finally {
                setCargando(false);
            }
        }

        cargarProducto();
    }, [id]);

    function obtenerEnlaceWhatsApp() {
        if (!producto) {
            return "#";
        }

        const numeroWhatsApp = "573112521403";

        const mensaje = [
            "Hola, estoy interesado en el siguiente producto:",
            "",
            producto.nombre,
            `SKU: ${producto.sku}`,
            "",
            "Quisiera consultar su disponibilidad."
        ].join("\n");

        return `https://wa.me/${numeroWhatsApp}?text=${encodeURIComponent(
            mensaje
        )}`;
    }

    if (cargando) {
        return (
            <>
                <Header />

                <main className="producto-detalle">
                    <div className="producto-detalle-cargando">
                        Cargando producto...
                    </div>
                </main>
            </>
        );
    }

    if (error || !producto) {
        return (
            <>
                <Header />

                <main className="producto-detalle">
                    <div className="producto-detalle-error">

                        <h1>
                            Producto no encontrado
                        </h1>

                        <p>
                            No pudimos encontrar el producto solicitado.
                        </p>

                        <Link
                            to={urlCatalogo}
                            className="producto-volver"
                        >
                            ← Volver al catálogo
                        </Link>

                    </div>
                </main>
            </>
        );
    }

    return (
        <>
            <Header />

            <main className="producto-detalle">

                <div className="producto-detalle-contenedor">

                    <div className="producto-detalle-imagen">

                        <img
                            src={logo}
                            alt=""
                            className="producto-detalle-logo"
                            aria-hidden="true"
                        />

                        {producto.en_descuento && (
                            <span className="producto-detalle-oferta">
                                Oferta
                            </span>
                        )}

                        <img
                            src={
                                producto.imagen_alta ||
                                producto.imagen
                            }
                            alt={producto.nombre}
                            className="producto-detalle-imagen-producto"
                        />

                    </div>


                    <div className="producto-detalle-info">

                        <span className="producto-detalle-categoria">
                            {producto.categoria}
                        </span>

                        <h1>
                            {producto.nombre}
                        </h1>

                        <div className="producto-detalle-precio">

                            <span>
                                $
                                {producto.precio_venta.toLocaleString(
                                    "es-CO"
                                )}
                            </span>

                        </div>

                        <div className="producto-detalle-separador" />


                        <div className="producto-detalle-datos">

                            {producto.sku && (
                                <div className="producto-dato">

                                    <span>
                                        SKU
                                    </span>

                                    <strong>
                                        {producto.sku}
                                    </strong>

                                </div>
                            )}

                            {producto.atributos?.tipo && (
                                <div className="producto-dato">

                                    <span>
                                        Tipo
                                    </span>

                                    <strong>
                                        {producto.atributos.tipo}
                                    </strong>

                                </div>
                            )}

                            {producto.atributos?.color && (
                                <div className="producto-dato">

                                    <span>
                                        Color
                                    </span>

                                    <strong>
                                        {producto.atributos.color}
                                    </strong>

                                </div>
                            )}

                            {producto.atributos?.estilo && (
                                <div className="producto-dato">

                                    <span>
                                        Estilo
                                    </span>

                                    <strong>
                                        {producto.atributos.estilo}
                                    </strong>

                                </div>
                            )}

                            {producto.atributos?.material && (
                                <div className="producto-dato">

                                    <span>
                                        Material
                                    </span>

                                    <strong>
                                        {producto.atributos.material}
                                    </strong>

                                </div>
                            )}

                        </div>


                        <a
                            href={obtenerEnlaceWhatsApp()}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="producto-whatsapp"
                        >
                            <svg
                                viewBox="0 0 24 24"
                                aria-hidden="true"
                            >
                                <path d="M20.5 11.6a8.5 8.5 0 0 1-12.6 7.5L3.5 20.5l1.4-4.2A8.5 8.5 0 1 1 20.5 11.6Z" />
                                <path d="M8.4 8.2c.2-.4.4-.4.7-.4h.5c.2 0 .4.1.5.4l.7 1.7c.1.3.1.5-.1.7l-.6.7c.7 1.2 1.6 2.1 2.8 2.8l.7-.6c.2-.2.4-.2.7-.1l1.7.7c.3.1.4.3.4.5v.5c0 .3 0 .5-.4.7-.4.2-1.4.5-2.7-.1-1.4-.6-3.1-1.7-4.3-3-1.2-1.2-2.4-2.9-3-4.3-.5-1.3-.3-2.3-.1-2.7Z" />
                            </svg>

                            <span>
                                Consultar disponibilidad
                            </span>

                            <span
                                className="producto-whatsapp-flecha"
                                aria-hidden="true"
                            >
                                →
                            </span>
                        </a>


                        <Link
                            to={urlCatalogo}
                            className="producto-volver"
                        >
                            ← Volver al catálogo
                        </Link>

                    </div>

                </div>

            </main>
        </>
    );
}

export default ProductoDetalle;