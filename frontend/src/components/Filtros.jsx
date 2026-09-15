function Filtros({
    opciones,
    filtros,
    onCambioFiltro,
    onLimpiarFiltros
}) {

    const hayFiltros =
        filtros.categoria ||
        filtros.tipo ||
        filtros.color ||
        filtros.estilo ||
        filtros.material ||
        filtros.precio_min ||
        filtros.precio_max;


    function renderOpciones(
        nombre,
        lista
    ) {

        if (!lista) {
            return null;
        }


        return lista.map(
            (item) => {

                const seleccionado =
                    filtros[nombre] === item.valor;


                return (
                    <option
                        key={item.valor}
                        value={item.valor}
                        disabled={
                            item.total === 0 &&
                            !seleccionado
                        }
                    >
                        {item.valor} ({item.total})
                    </option>
                );

            }
        );
    }


    return (
        <div className="filtros">


            {/* =====================================
                CABECERA
            ===================================== */}

            <div className="filtros-top">

                <span className="filtros-label">
                    Filtrar por
                </span>


                {hayFiltros && (

                    <button
                        type="button"
                        className="filtros-limpiar"
                        onClick={onLimpiarFiltros}
                    >
                        Limpiar filtros
                    </button>

                )}

            </div>


            {/* =====================================
                CONTROLES
            ===================================== */}

            <div className="filtros-controles">


                {/* CATEGORÍA */}

                <div className="filtro">

                    <label htmlFor="filtro-categoria">
                        Categoría
                    </label>


                    <select
                        id="filtro-categoria"
                        value={filtros.categoria}
                        onChange={(e) =>
                            onCambioFiltro(
                                "categoria",
                                e.target.value
                            )
                        }
                    >

                        <option value="">
                            Todas
                        </option>


                        {renderOpciones(
                            "categoria",
                            opciones?.categoria
                        )}

                    </select>

                </div>


                {/* TIPO */}

                <div className="filtro">

                    <label htmlFor="filtro-tipo">
                        Tipo
                    </label>


                    <select
                        id="filtro-tipo"
                        value={filtros.tipo}
                        onChange={(e) =>
                            onCambioFiltro(
                                "tipo",
                                e.target.value
                            )
                        }
                    >

                        <option value="">
                            Todos
                        </option>


                        {renderOpciones(
                            "tipo",
                            opciones?.tipo
                        )}

                    </select>

                </div>


                {/* COLOR */}

                <div className="filtro">

                    <label htmlFor="filtro-color">
                        Color
                    </label>


                    <select
                        id="filtro-color"
                        value={filtros.color}
                        onChange={(e) =>
                            onCambioFiltro(
                                "color",
                                e.target.value
                            )
                        }
                    >

                        <option value="">
                            Todos
                        </option>


                        {renderOpciones(
                            "color",
                            opciones?.color
                        )}

                    </select>

                </div>


                {/* ESTILO */}

                <div className="filtro">

                    <label htmlFor="filtro-estilo">
                        Estilo
                    </label>


                    <select
                        id="filtro-estilo"
                        value={filtros.estilo}
                        onChange={(e) =>
                            onCambioFiltro(
                                "estilo",
                                e.target.value
                            )
                        }
                    >

                        <option value="">
                            Todos
                        </option>


                        {renderOpciones(
                            "estilo",
                            opciones?.estilo
                        )}

                    </select>

                </div>


                {/* MATERIAL */}

                <div className="filtro">

                    <label htmlFor="filtro-material">
                        Material
                    </label>


                    <select
                        id="filtro-material"
                        value={filtros.material}
                        onChange={(e) =>
                            onCambioFiltro(
                                "material",
                                e.target.value
                            )
                        }
                    >

                        <option value="">
                            Todos
                        </option>


                        {renderOpciones(
                            "material",
                            opciones?.material
                        )}

                    </select>

                </div>


                {/* PRECIO */}

                <div className="filtro filtro-precio">

                    <label>
                        Precio
                    </label>


                    <div className="filtros-precio">

                        <input
                            type="number"
                            min="0"
                            placeholder="Mín."
                            value={
                                filtros.precio_min
                            }
                            onChange={(e) =>
                                onCambioFiltro(
                                    "precio_min",
                                    e.target.value
                                )
                            }
                        />


                        <span>
                            —
                        </span>


                        <input
                            type="number"
                            min="0"
                            placeholder="Máx."
                            value={
                                filtros.precio_max
                            }
                            onChange={(e) =>
                                onCambioFiltro(
                                    "precio_max",
                                    e.target.value
                                )
                            }
                        />

                    </div>

                </div>

            </div>

        </div>
    );
}


export default Filtros;