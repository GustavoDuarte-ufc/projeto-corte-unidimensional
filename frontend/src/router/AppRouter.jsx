import {
    BrowserRouter,
    Routes,
    Route,
    Navigate
} from "react-router-dom";

import Login
    from "../pages/Login";

import Dashboard
    from "../pages/Dashboard";

import ProtectedRoute
    from "../components/ProtectedRoute";

import CutOptimizer
    from "../components/CutOptimizer";

export default function
AppRouter(){

    return(

        <BrowserRouter>

            <Routes>

                <Route
                    path="/login"
                    element={<Login/>}
                />

                <Route
                    path="/"
                    element={
                        <ProtectedRoute>
                            <Dashboard/>
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/calculator"
                    element={<Navigate to="/cut-optimizer" replace />}
                />

                <Route

                    path="/cut-optimizer"

                    element={
                        <ProtectedRoute>
                            <CutOptimizer/>
                        </ProtectedRoute>
                    }
                />

            </Routes>

        </BrowserRouter>
    );
}