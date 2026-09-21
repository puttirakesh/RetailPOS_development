import axios from "axios";

// No, you do not need to change these constants unless your backend/API uses different keys for storing the tokens or user info in localStorage.
// These keys are used within the frontend app to save and retrieve authentication/session information.
// If you're using Postman to test your API, you likely saw "access_token", "refresh_token", "username", "role", "user_id" as fields in the login or token responses.
// The frontend expects this structure and uses these keys to store values to localStorage. Only change them if your API uses different names.
// The values for these (`access_token`, `refresh_token`) are received from your backend upon login/auth.

// Current keys used to store session info in localStorage:
const TOKEN_KEY = "retailpos_access_token";
const REFRESH_KEY = "retailpos_refresh_token";
const USER_KEY = "retailpos_user";

export const tokenStore = {
  getAccess: () => localStorage.getItem(TOKEN_KEY),
  getRefresh: () => localStorage.getItem(REFRESH_KEY),
  getUser: () => {
    try {
      const raw = localStorage.getItem(USER_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  },
  setSession: ({ access_token, refresh_token, username, role, user_id }) => {
    localStorage.setItem(TOKEN_KEY, access_token);
    if (refresh_token) localStorage.setItem(REFRESH_KEY, refresh_token);
    localStorage.setItem(
      USER_KEY,
      JSON.stringify({ username, role, user_id })
    );
  },
  clear: () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_KEY);
    localStorage.removeItem(USER_KEY);
  },
};

const api = axios.create({
  baseURL: "/api/v1",
  timeout: 20000,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const token = tokenStore.getAccess();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (error) => {
    if (error.response?.status === 401) {
      tokenStore.clear();
      if (!window.location.pathname.includes("/login")) {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;