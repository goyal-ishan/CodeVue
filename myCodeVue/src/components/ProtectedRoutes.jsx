
import { Navigate, Outlet } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

const ProtectedRoute = () => {
    const token = localStorage.getItem("accessToken");

    if (!token) {
        return <Navigate to="/Login" replace />;
    }

    try {
        const decoded = jwtDecode(token);

        if (!decoded.exp || decoded.exp * 1000 <= Date.now()) {
            localStorage.removeItem("accessToken");
            return <Navigate to="/Login" replace />;
        }
    } catch {
        localStorage.removeItem("accessToken");
        return <Navigate to="/Login" replace />;
    }

    return <Outlet />;
};

export default ProtectedRoute;
