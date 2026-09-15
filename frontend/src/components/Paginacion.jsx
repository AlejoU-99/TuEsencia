function Paginacion({
    pagina,
    totalPaginas,
    onCambiarPagina
}) {
    if (totalPaginas <= 1) {
        return null;
    }

    function obtenerPaginas() {
        const paginas = [];

        if (totalPaginas <= 7) {
            for (let i = 1; i <= totalPaginas; i++) {
                paginas.push(i);
            }

            return paginas;
        }

        paginas.push(1);

        if (pagina > 4) {
            paginas.push("...");
        }

        const inicio = Math.max(2, pagina - 2);
        const fin = Math.min(totalPaginas - 1, pagina + 2);

        for (let i = inicio; i <= fin; i++) {
            paginas.push(i);
        }

        if (pagina < totalPaginas - 3) {
            paginas.push("...");
        }

        paginas.push(totalPaginas);

        return paginas;
    }

    const paginas = obtenerPaginas();

    return (
        <nav
            className="paginacion"
            aria-label="Paginación del catálogo"
        >
            <button
                type="button"
                className="paginacion-boton paginacion-anterior"
                onClick={() => onCambiarPagina(pagina - 1)}
                disabled={pagina === 1}
            >
                <span aria-hidden="true">←</span>
                <span>Anterior</span>
            </button>

            <div className="paginacion-numeros">
                {paginas.map((numero, indice) => {
                    if (numero === "...") {
                        return (
                            <span
                                key={`ellipsis-${indice}`}
                                className="paginacion-ellipsis"
                                aria-hidden="true"
                            >
                                ...
                            </span>
                        );
                    }

                    return (
                        <button
                            key={numero}
                            type="button"
                            className={
                                numero === pagina
                                    ? "paginacion-numero activo"
                                    : "paginacion-numero"
                            }
                            onClick={() =>
                                onCambiarPagina(numero)
                            }
                            aria-current={
                                numero === pagina
                                    ? "page"
                                    : undefined
                            }
                        >
                            {numero}
                        </button>
                    );
                })}
            </div>

            <button
                type="button"
                className="paginacion-boton paginacion-siguiente"
                onClick={() => onCambiarPagina(pagina + 1)}
                disabled={pagina === totalPaginas}
            >
                <span>Siguiente</span>
                <span aria-hidden="true">→</span>
            </button>
        </nav>
    );
}

export default Paginacion;