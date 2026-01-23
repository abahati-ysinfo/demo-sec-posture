import { useState, useEffect, createContext, useContext, ReactNode } from 'react';
import Cookies from 'js-cookie';
import { authAPI, setCSRFToken } from './api';

interface User {
  id: string;
  email: string;
  full_name: string;
  company_name: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAdmin: boolean;
  login: (
    email: string,
    password: string
  ) => Promise<{ access_token: string; user: User; csrf_token?: string }>;
  register: (data: {
    email: string;
    password: string;
    full_name: string;
    company_name: string;
  }) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const ENABLE_COOKIE_AUTH = process.env.NEXT_PUBLIC_ENABLE_COOKIE_AUTH === 'true';
const ENABLE_CSRF = process.env.NEXT_PUBLIC_ENABLE_CSRF === 'true';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined' && !ENABLE_COOKIE_AUTH) {
      Cookies.remove('access_token');
    }

    if (ENABLE_COOKIE_AUTH) {
      authAPI
        .getCurrentUser()
        .then((response) => {
          setUser(response.data);
          if (response.data.is_admin) {
            setIsAdmin(true);
          }
          setIsLoading(false);

          if (ENABLE_CSRF) {
            authAPI
              .getCSRFToken()
              .then((csrfResponse) => {
                setCSRFToken(csrfResponse.data.csrf_token);
              })
              .catch(() => {
                console.error('Failed to fetch CSRF token');
              });
          }
        })
        .catch(() => {
          setIsLoading(false);
        });
    } else {
      if (typeof window !== 'undefined') {
        const storedToken = localStorage.getItem('auth_token');
        if (storedToken) {
          const { setAuthToken } = require('./api');
          setAuthToken(storedToken);

          authAPI
            .getCurrentUser()
            .then((response) => {
              setUser(response.data);
              if (response.data.is_admin) {
                setIsAdmin(true);
              }
              setIsLoading(false);
            })
            .catch(() => {
              localStorage.removeItem('auth_token');
              setIsLoading(false);
            });
        } else {
          setIsLoading(false);
        }
      } else {
        setIsLoading(false);
      }
    }
  }, []);

  const login = async (email: string, password: string) => {
    const response = await authAPI.login({ email, password });

    if (ENABLE_COOKIE_AUTH) {
      if (ENABLE_CSRF && response.data.csrf_token) {
        setCSRFToken(response.data.csrf_token);
      }

      const meResponse = await authAPI.getCurrentUser();
      setUser(meResponse.data);
      if (meResponse.data.is_admin) {
        setIsAdmin(true);
      }
    } else {
      const { access_token, user: userData } = response.data;

      const { setAuthToken } = await import('./api');
      setAuthToken(access_token);

      if (typeof window !== 'undefined') {
        Cookies.remove('access_token');
      }

      try {
        const tokenPayload = JSON.parse(atob(access_token.split('.')[1]));
        if (tokenPayload.is_admin) {
          setIsAdmin(true);
        } else if (userData && userData.is_admin) {
          setIsAdmin(true);
          setUser(userData);
        } else {
          setUser(userData);
          setIsAdmin(false);
        }
      } catch {
        if (userData && userData.is_admin) {
          setIsAdmin(true);
        }
        setUser(userData);
        setIsAdmin(false);
      }
    }

    return response.data;
  };

  const register = async (data: {
    email: string;
    password: string;
    full_name: string;
    company_name: string;
  }) => {
    const response = await authAPI.register(data);

    if (ENABLE_COOKIE_AUTH) {
      if (ENABLE_CSRF && response.data.csrf_token) {
        setCSRFToken(response.data.csrf_token);
      }

      const meResponse = await authAPI.getCurrentUser();
      setUser(meResponse.data);
      if (meResponse.data.is_admin) {
        setIsAdmin(true);
      }
    } else {
      const { access_token, user: userData } = response.data;

      const { setAuthToken } = await import('./api');
      setAuthToken(access_token);

      if (typeof window !== 'undefined') {
        Cookies.remove('access_token');
      }

      setUser(userData);
    }
  };

  const logout = async () => {
    if (ENABLE_COOKIE_AUTH) {
      try {
        await authAPI.logout();
      } catch (error) {
        console.error('Logout error:', error);
      }
    } else {
      const { setAuthToken } = await import('./api');
      setAuthToken(null);

      if (typeof window !== 'undefined') {
        Cookies.remove('access_token');
      }
    }
    setCSRFToken(null);
    setUser(null);
    setIsAdmin(false);
    if (typeof window !== 'undefined') {
      window.location.href = '/';
    }
  };

  const contextValue: AuthContextType = {
    user,
    isLoading,
    isAdmin,
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={contextValue}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
