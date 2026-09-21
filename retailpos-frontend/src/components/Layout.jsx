import { useState } from "react";
import { Outlet, useLocation } from "react-router-dom";
import Sidebar from "./Sidebar";
import Navbar from "./Navbar";

const titles = {
  "/": "Dashboard",
  "/masters/brands": "Brands",
  "/masters/products": "Products",
  "/masters/customers": "Customers",
  "/masters/suppliers": "Suppliers",
  "/masters/categories": "Categories",
  "/masters/states": "Locations",
};

export default function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { pathname } = useLocation();
  const title = titles[pathname] || "RetailPOS";

  return (
    <div className="min-h-screen flex bg-base-200">
      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar title={title} onMenuClick={() => setSidebarOpen(true)} />
        <main className="flex-1 p-4 lg:p-6 overflow-auto">
          <div className="page-enter max-w-7xl mx-auto">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}