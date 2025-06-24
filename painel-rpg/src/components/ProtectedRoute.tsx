import React from "react";
import { useAuth } from "../context/AuthContext";

export const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, loading, login } = useAuth();

  if (loading) return <div>Carregando...</div>;
  if (!user) {
    login();
    return <div>Redirecionando para login...</div>;
  }
  return <>{children}</>;
};
