import verticalLogo from "../assets/vertical 2.png";


function InstagramIcon() {
    return (
        <svg
            viewBox="0 0 24 24"
            aria-hidden="true"
        >
            <rect
                x="3"
                y="3"
                width="18"
                height="18"
                rx="5"
            />

            <circle
                cx="12"
                cy="12"
                r="4"
            />

            <circle
                cx="17.5"
                cy="6.5"
                r="1"
                className="social-icon-dot"
            />
        </svg>
    );
}


function FacebookIcon() {
    return (
        <svg
            viewBox="0 0 24 24"
            aria-hidden="true"
        >
            <path
                d="M14 8h3V4h-3c-3.3 0-5 1.9-5 5v3H6v4h3v4h4v-4h3l1-4h-4V9c0-.7.3-1 1-1Z"
                className="facebook-shape"
            />
        </svg>
    );
}


function WhatsAppIcon() {
    return (
        <svg
            viewBox="0 0 24 24"
            aria-hidden="true"
        >
            <path
                d="M20.1 11.7a8 8 0 0 1-11.8 7l-4.1 1.1 1.1-4A8 8 0 1 1 20.1 11.7Z"
            />

            <path
                d="M8.5 8.2c.2-.4.4-.4.7-.4h.5c.2 0 .4.1.5.4l.7 1.6c.1.2.1.4-.1.6l-.5.6c-.1.1-.1.3 0 .5.4.7 1 1.3 1.7 1.7.2.1.4.1.5 0l.6-.6c.2-.2.4-.2.6-.1l1.6.7c.3.1.4.3.4.5v.5c0 .3 0 .5-.4.7-.4.2-1.1.3-1.5.2-1-.2-2.2-.8-3.4-1.9-1.1-1-1.8-2.2-2-3.2-.1-.5 0-1.1.1-1.8Z"
                className="whatsapp-inner"
            />
        </svg>
    );
}


function TrustIcon({ tipo }) {

    if (tipo === "seguridad") {

        return (
            <svg
                viewBox="0 0 24 24"
                aria-hidden="true"
            >
                <path d="M12 3 19 6v5c0 4.5-2.8 8.1-7 10-4.2-1.9-7-5.5-7-10V6l7-3Z" />
                <path d="m9 12 2 2 4-4" />
            </svg>
        );

    }


    if (tipo === "atencion") {

        return (
            <svg
                viewBox="0 0 24 24"
                aria-hidden="true"
            >
                <circle
                    cx="12"
                    cy="12"
                    r="8"
                />

                <path d="M8 13c.7 2 2 3 4 3s3.3-1 4-3" />

                <path d="M9 9h.01" />
                <path d="M15 9h.01" />
            </svg>
        );

    }


    return (
        <svg
            viewBox="0 0 24 24"
            aria-hidden="true"
        >
            <path d="M3 7h11v10H3z" />
            <path d="M14 10h4l3 3v4h-7z" />
            <circle
                cx="7"
                cy="18"
                r="2"
            />
            <circle
                cx="18"
                cy="18"
                r="2"
            />
        </svg>
    );
}


function Footer() {

    return (
        <footer className="site-footer">

            <div className="footer-container">


                {/* =====================================
                    PARTE PRINCIPAL
                ===================================== */}

                <div className="footer-main">


                    {/* MARCA */}

                    <div className="footer-brand">

                        <img
                            src={verticalLogo}
                            alt="TuEsencia"
                            className="footer-logo"
                        />

                    </div>


                    {/* NAVEGACIÓN */}

                    <div className="footer-column">

                        <span className="footer-heading">
                            Explorar
                        </span>

                        <nav className="footer-navigation">

                            <a href="/">
                                Catálogo
                            </a>

                            <a href="/#nosotros">
                                Nosotros
                            </a>

                        </nav>

                    </div>


                    {/* REDES */}

                    <div className="footer-column">

                        <span className="footer-heading">
                            Síguenos
                        </span>


                        <div className="footer-social">


                            {/* INSTAGRAM */}

                            <span
                                className="footer-social-item"
                                title="Instagram próximamente"
                                aria-label="Instagram próximamente"
                            >

                                <InstagramIcon />

                                <span>
                                    Instagram
                                </span>

                            </span>


                            {/* FACEBOOK */}

                            <span
                                className="footer-social-item"
                                title="Facebook próximamente"
                                aria-label="Facebook próximamente"
                            >

                                <FacebookIcon />

                                <span>
                                    Facebook
                                </span>

                            </span>


                            {/* WHATSAPP */}

                            <a
                                href="https://wa.me/573112521403"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="footer-social-item"
                                aria-label="Contactar por WhatsApp"
                            >

                                <WhatsAppIcon />

                                <span>
                                    WhatsApp
                                </span>

                            </a>

                        </div>

                    </div>

                </div>


                {/* =====================================
                    INDICADORES DE CONFIANZA
                ===================================== */}

                <div className="footer-trust">


                    <div className="footer-trust-item">

                        <TrustIcon tipo="seguridad" />

                        <div>

                            <strong>
                                Compra segura
                            </strong>

                            <span>
                                Una experiencia confiable
                            </span>

                        </div>

                    </div>


                    <div className="footer-trust-item">

                        <TrustIcon tipo="atencion" />

                        <div>

                            <strong>
                                Atención personalizada
                            </strong>

                            <span>
                                Estamos para ayudarte
                            </span>

                        </div>

                    </div>


                    <div className="footer-trust-item">

                        <TrustIcon tipo="envio" />

                        <div>

                            <strong>
                                Envíos nacionales
                            </strong>

                            <span>
                                Llevamos TuEsencia contigo
                            </span>

                        </div>

                    </div>

                </div>


                {/* =====================================
                    COPYRIGHT
                ===================================== */}

                <div className="footer-bottom">

                    <span>
                        © 2026 TuEsencia
                    </span>

                    <span>
                        Todos los derechos reservados
                    </span>

                </div>

            </div>

        </footer>
    );
}


export default Footer;