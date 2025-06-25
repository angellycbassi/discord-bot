'use client';

import React, { createContext, useContext, useEffect, useState } from "react";
import { fetchUser } from "../utils/api";

export type User = {
  id: string;
  discord_id?: string; // Adicionado para integração real
  username: string;
  avatar?: string;
  servers?: string[];
  xp?: number;
  level?: number;
  achievements?: string[];
  isAdmin?: boolean;
};

type AuthContextType = {
  user: User | null;
  loading: boolean;
  login: () => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
    const sessionId = typeof window !== "undefined" ? localStorage.getItem("session_id") : undefined;
    if (sessionId) {
      fetchUser(sessionId)
        .then(u => {
          setUser(u);
          if (u.discord_id) localStorage.setItem("discord_id", u.discord_id);
        })
        .catch(() => setUser(null))
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = () => {
    window.location.href = "/api/auth";
  };

  const logout = () => {
    localStorage.removeItem("session_id");
    localStorage.removeItem("discord_id");
    window.location.reload();
  };

  if (!isClient) return null; // Hydration guard: só renderiza no client

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth deve ser usado dentro de AuthProvider");
  return ctx;
};
