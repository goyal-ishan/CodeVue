import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

export default function ProtectedRoute() {
  const { user } = useAuth();

  // Validate stored tokens against literal "null" / "undefined" strings
  const rawToken = localStorage.getItem("token") || localStorage.getItem("authToken");
  const rawEmail = localStorage.getItem("userEmail") || localStorage.getItem("email");

  const hasValidToken = rawToken && rawToken !== "null" && rawToken !== "undefined";
  const hasValidEmail = rawEmail && rawEmail !== "null" && rawEmail !== "undefined";

  const isAuthenticated = Boolean(user?.email || (hasValidToken && hasValidEmail));

  if (!isAuthenticated) {
    
    return <Navigate to="/Login" replace />;
  }

  return <Outlet />;
}