import { useContext } from "react";
import { AuthContext } from "../context/authContext";

let globalLogoutHandler: (() => void) | null = null;

export const setGlobalLogoutHandler = (handler: () => void) => {
  globalLogoutHandler = handler;
};

export const clearGlobalLogoutHandler = () => {
  globalLogoutHandler = null;
};

export const handleUnauthenticated = () => {
  if (globalLogoutHandler) {
    globalLogoutHandler();
  }
};


export const useAuth = () => useContext(AuthContext);
