import { HashRouter, Routes, Route, useLocation } from "react-router-dom";
import { useEffect } from "react";

import Catalogo from "./pages/Catalogo";
import ProductoDetalle from "./pages/ProductoDetalle";
import Nosotros from "./pages/Nosotros";
import Footer from "./components/Footer";

function ScrollManager() {
    const location = useLocation();

    useEffect(() => {
        if (location.pathname.startsWith("/producto/") || location.pathname === "/nosotros") {
            window.scrollTo(0, 0);
        }
    }, [location.pathname]);

    return null;
}

function App() {
    return (
        <HashRouter>
            <ScrollManager />

            <Routes>
                <Route
                    path="/"
                    element={
                        <>
                            <Catalogo />
                            <Footer />
                        </>
                    }
                />

                <Route
                    path="/producto/:id"
                    element={
                        <>
                            <ProductoDetalle />
                            <Footer />
                        </>
                    }
                />

                <Route
                    path="/nosotros"
                    element={
                        <>
                            <Nosotros />
                            <Footer />
                        </>
                    }
                />
            </Routes>
        </HashRouter>
    );
}

export default App;