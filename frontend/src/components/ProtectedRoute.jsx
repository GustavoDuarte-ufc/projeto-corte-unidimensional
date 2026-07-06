import {
    Navigate
} from "react-router-dom";

import {
    useAuth
} from "../hooks/useAuth";

export default function
ProtectedRoute(
    {children}
){

    const {
        authenticated,
        loading
    } = useAuth();

    if(loading){

        return(
            <h2>
                Carregando...
            </h2>
        );
    }

    return authenticated
        ? children
        : <Navigate to="/login"/>;
}