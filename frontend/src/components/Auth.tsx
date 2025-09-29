import React, { createContext, useState, useContext, useEffect, useCallback } from "react";
import type { UUIDTypes } from "uuid";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import api from "../utils/api";

const API_URL = import.meta.env.VITE_API_URL;

type User = {
    id: UUIDTypes;
    email: string;
    username: string;
    recipes: [] | null;
};

type AuthContextType = {
    user: User | null;
    isLoggedIn: boolean;
    isLoading: boolean;
    error: string | null;
    login: (email: string, password: string) => Promise<void>;
    logout: () => void;
    authGet: (url: string) => Promise<any>;

};

const AuthContext = createContext<AuthContextType>({
    user: null,
    isLoggedIn: false,
    isLoading: false,
    error: null,
    login: async () => {},
    logout: () => {},
    authGet: async () => { throw new Error('Not implemented') },
});

let globalLogoutHandler: (() => void) | null = null;

export const handleUnauthenticated = () => {
  if (globalLogoutHandler) {
    globalLogoutHandler();
  }
};

import type { ReactNode } from "react";

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const navigate = useNavigate();

    useEffect(() => {
        const checkAuth = async () => {
          const token = sessionStorage.getItem('auth_token');
          if (token) {
            setIsLoading(true);
            try {
              const { data } = await api.get(`${API_URL}/users/current`);
              setUser(data);
              setIsLoggedIn(true);
            } catch (error) {
              console.error("Auth token invalid:", error);
              sessionStorage.removeItem('auth_token');
            } finally {
              setIsLoading(false);
            }
          }
        };

        checkAuth();
      }, []);

    const login = async (email: string, password: string) => {
        setIsLoading(true);
        setError(null);
        try {
            let loginPayload = new URLSearchParams()
            loginPayload.append("username", email)
            loginPayload.append("password", password)

            const response = await axios.post(`${API_URL}/auth/token`,
                loginPayload
            );

            const token = response.data.access_token;
            sessionStorage.setItem("auth_token", token);

            const { data } = await api.get(`${API_URL}/users/current`)

            setIsLoggedIn(true)
            setUser(data)
        } catch (error: any) {
            console.error("Error: ", error.message)
            setError("Login failed: Invalid password or username");
            throw new Error("Login failed: Invalid password or username")
        } finally {
            setIsLoading(false);
          }
        };

        const authGet = async (url: string) => {
            const token = sessionStorage.getItem('auth_token');
            if (!token)
                throw new Error('Not authenticated');

            return axios.get(url, {
                headers: {
                  Authorization: `Bearer ${token}`
                }
              });
        }

        const logout = useCallback(async () => {
            if (!isLoggedIn)
				return;

			setUser(null);
			setIsLoggedIn(false);

            try {
				const response = await api.post(`${API_URL}/auth/logout`);
                console.log(response.data)
            } catch (error) {
				console.error("Logout error:", error);
            } finally {
				sessionStorage.removeItem('auth_token');
                navigate("/");
            }
        }, [navigate, isLoggedIn]);


        useEffect(() => {
            globalLogoutHandler = logout;
            return () => {
                globalLogoutHandler = null;
            };
        }, [logout]);

    return (
        <AuthContext.Provider
        value={{
            user,
            isLoggedIn,
            isLoading,
            error,
            login,
            logout,
            authGet
            }}
        >
            {children}
        </AuthContext.Provider>
    )
}

export const useAuth = () => useContext(AuthContext)
