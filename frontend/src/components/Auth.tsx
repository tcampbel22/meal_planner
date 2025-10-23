import { useState, useEffect, useCallback } from "react";
import axios, { AxiosError } from "axios";
import { useNavigate } from "react-router-dom";
import api from "../utils/api";
import { setGlobalLogoutHandler, clearGlobalLogoutHandler } from "../utils/authUtils";
import type { ReactNode } from "react";
import { AuthContext } from "../context/authContext";
import type { User } from "../context/authContext";
import type { AxiosResponse } from "axios";

const API_URL = import.meta.env.VITE_API_URL;


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
              const { data } = await api.get(`${API_URL}/users/me`);
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
            const loginPayload = new URLSearchParams()
            loginPayload.append("username", email)
            loginPayload.append("password", password)

            const response = await axios.post(`${API_URL}/auth/token`,
                loginPayload
            );

            const token = response.data.access_token;
            sessionStorage.setItem("auth_token", token);

            const { data } = await api.get(`/users/me`)

            setIsLoggedIn(true)
            setUser(data)
        } catch (error: unknown) {
            console.error("Error: ", error);

            if (axios.isAxiosError(error)) {
                const axiosError = error as AxiosError;
                console.error("Error message:", axiosError.message);

                if (axiosError.response?.status === 401) {
                    setError("Login failed: Invalid password or username");
                } else {
                    setError(`Login failed: ${axiosError.message}`);
                }
            } else {
                setError("Login failed: An unexpected error occurred");
            }

            throw new Error("Login failed: Invalid credentials or server error");
        } finally {
            setIsLoading(false);
          }
        };

        const authGet = async (url: string): Promise<AxiosResponse> => {
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
            } catch (error: unknown) {
				console.error("Logout error:", error);
            } finally {
				sessionStorage.removeItem('auth_token');
                navigate("/");
            }
        }, [navigate, isLoggedIn]);


        useEffect(() => {
            setGlobalLogoutHandler(logout);
            return () => {
                clearGlobalLogoutHandler();
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
