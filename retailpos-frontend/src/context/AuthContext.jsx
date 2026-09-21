import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
} from "react";
import { login as apiLogin } from "../api/auth";
import { tokenStore } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => tokenStore.getUser());
  const [token, setToken] = useState(() => tokenStore.getAccess());

  const isAuthenticated = Boolean(token);

  const login = useCallback(async (username, password) => {
    const data = await apiLogin(username, password);
    tokenStore.setSession(data);
    setToken(data.access_token);
    setUser({
      username: data.username,
      role: data.role,
      user_id: data.user_id,
    });
    return data;
  }, []);

  const logout = useCallback(() => {
    tokenStore.clear();
    setToken(null);
    setUser(null);
  }, []);

  const value = useMemo(
    () => ({ user, token, isAuthenticated, login, logout }),
    [user, token, isAuthenticated, login, logout]
  );

  return (
    <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}