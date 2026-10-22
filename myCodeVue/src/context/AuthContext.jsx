import { createContext, useContext, useState } from "react";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    try {
      const storedUser = localStorage.getItem("user");
      if (storedUser) {
        return JSON.parse(storedUser);
      }
    } catch (e) {
      console.log(e);
    }

    const email =
      localStorage.getItem("userEmail") || localStorage.getItem("email");
    const fullName =
      localStorage.getItem("userName") || localStorage.getItem("name");
    const token =
      localStorage.getItem("token") || localStorage.getItem("authToken");

    // Only authenticate if email or token exists
    if (email || token) {
      return {
        fullName: fullName || "Candidate",
        email: email || "",
        token: token || "",
      };
    }

    return null;
  });

  const login = (userData) => {
    if (userData.token) localStorage.setItem("token", userData.token);
    if (userData.email) localStorage.setItem("userEmail", userData.email);
    if (userData.fullName) localStorage.setItem("userName", userData.fullName);
    localStorage.setItem("user", JSON.stringify(userData));
    setUser(userData);
  };

  const logout = () => {
    // 1. Wipe all possible auth keys from localStorage
    localStorage.removeItem("token");
    localStorage.removeItem("authToken");
    localStorage.removeItem("jwt");
    localStorage.removeItem("user");
    localStorage.removeItem("userEmail");
    localStorage.removeItem("email");
    localStorage.removeItem("userName");
    localStorage.removeItem("name");
    localStorage.removeItem("userId");

    // 2. Clear React state in memory
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, setUser, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);