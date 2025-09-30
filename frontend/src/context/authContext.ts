import { createContext } from "react";
import type { UUIDTypes } from "uuid";
import type { AxiosResponse } from "axios";

export type User = {
    id: UUIDTypes;
    email: string;
    username: string;
    recipes: [] | null;
};

export type AuthContextType = {
    user: User | null;
    isLoggedIn: boolean;
    isLoading: boolean;
    error: string | null;
    login: (email: string, password: string) => Promise<void>;
    logout: () => void;
    authGet: (url: string) => Promise<AxiosResponse>;
};

export const AuthContext = createContext<AuthContextType>({
    user: null,
    isLoggedIn: false,
    isLoading: false,
    error: null,
    login: async () => {},
    logout: () => {},
    authGet: async () => { throw new Error('Not implemented') },
});
