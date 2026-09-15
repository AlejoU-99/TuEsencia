import { Link, useLocation } from "react-router-dom";

import logo from "../assets/logo.png";


function ProductoCard({ producto }) {

    const location = useLocation();

    const {
        id,
        nombre,
        precio_venta,
        en_descuento,
        categoria,
        imagen,
        atributos
    } = producto;


    return (
        <Link
            to={{
                pathname: `/producto/${id}`,
                search: location.search
            }}
            className="producto-card"
        >

            <div className="producto-imagen-container">

                {/* LOGO DE MARCA */}

                <img
                    src={logo}
                    alt=""
                    className="producto-logo"
                    aria-hidden="true"
                />


                {/* OFERTA */}

                {en_descuento && (

                    <span className="producto-descuento">
                        Oferta
                    </span>

                )}


                {/* IMAGEN DEL PRODUCTO */}

                <img
                    src={imagen}
                    alt={nombre}
                    className="producto-imagen"
                    loading="lazy"
                />

            </div>


            {/* INFORMACIÓN */}

            <div className="producto-info">

                <span className="producto-categoria">
                    {categoria}
                </span>


                <h3 className="producto-nombre">
                    {nombre}
                </h3>


                <div className="producto-precio">

                    <span className="precio-venta">
                        $
                        {precio_venta.toLocaleString("es-CO")}
                    </span>

                </div>


                {atributos?.color && (

                    <span className="producto-atributo">
                        {atributos.color}
                    </span>

                )}

            </div>

        </Link>
    );
}


export default ProductoCard;