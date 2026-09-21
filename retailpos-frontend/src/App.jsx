import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";
import Layout from "./components/Layout";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Brands from "./pages/masters/Brands";
import Placeholder from "./pages/Placeholder";

import Products from "./pages/masters/Products";
import Customers from "./pages/masters/Customers";
import Categories from "./pages/masters/Categories";
import Suppliers from "./pages/masters/Suppliers";


const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: 1, refetchOnWindowFocus: false },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route
              element={
                <ProtectedRoute>
                  <Layout />
                </ProtectedRoute>
              }
            >
              <Route path="/" element={<Dashboard />} />
              <Route path="/masters/brands" element={<Brands />} />
              <Route path="/masters/products" element={<Products />} />
              <Route path="/masters/customers" element={<Customers />} />
              <Route path="/masters/categories" element={<Categories />} />
              <Route path="/masters/suppliers" element={<Suppliers />} />
              <Route
                path="/masters/states"
                element={<Placeholder name="Locations" />}
              />
            </Route>
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}
