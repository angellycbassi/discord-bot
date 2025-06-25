import React, { createContext, useContext, useEffect, useState } from 'react';
import { fetchUser } from '../utils/api';

export interface User {
  id: string;
  username: string;
  avatar: string;
  discordId: string;
  isAdmin: boolean;
  servers: string[];
  economy: {
    coins: number;
    bank: number;
    history: any[];
  };
  characters: any[];
}

interface AuthContextData {
  user: User | null;
  loading: boolean;
  error: string | null;
  login: () => Promise<void>;
  logout: () => Promise<void>;
  updateUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextData>({} as AuthContextData);

export const AuthProvider: React.FC<{children: React.ReactNode}> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const updateUser = async () => {
    try {
      const userData = await fetchUser();
      setUser(userData);
    } catch (err) {
      console.error('Error fetching user:', err);
      setError(err instanceof Error ? err.message : 'Failed to fetch user data');
    }
  };

  useEffect(() => {
    updateUser().finally(() => setLoading(false));
  }, []);

  // Login padrão: redireciona para rota de login OAuth
  const handleLogin = async () => {
    window.location.href = '/api/auth/login';
  };

  // Logout padrão: redireciona para rota de logout OAuth
  const handleLogout = async () => {
    window.location.href = '/api/auth/logout';
    setUser(null);
    setError(null);
  };

  return (
    <AuthContext.Provider 
      value={{
        user,
        loading,
        error,
        login: handleLogin,
        logout: handleLogout,
        updateUser
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
