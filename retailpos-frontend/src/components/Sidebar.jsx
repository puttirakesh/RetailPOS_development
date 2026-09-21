import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Tags,
  Package,
  Users,
  Truck,
  MapPin,
  Layers,
  LogOut,
  Store,
} from "lucide-react";
import { useAuth } from "../context/AuthContext";

const links = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/masters/brands", label: "Brands", icon: Tags },
  { to: "/masters/products", label: "Products", icon: Package },
  { to: "/masters/customers", label: "Customers", icon: Users },
  { to: "/masters/suppliers", label: "Suppliers", icon: Truck },
  { to: "/masters/categories", label: "Categories", icon: Layers },
  { to: "/masters/states", label: "Locations", icon: MapPin },
];

export default function Sidebar({ open, onClose }) {
  const { logout, user } = useAuth();

  return (
    <>
      <div
        className={`fixed inset-0 z-40 bg-black/40 backdrop-blur-[2px] lg:hidden transition-opacity duration-300 ${
          open ? "opacity-100" : "opacity-0 pointer-events-none"
        }`}
        onClick={onClose}
      />

      <aside
        className={`fixed lg:sticky top-0 left-0 z-50 h-screen w-72 flex flex-col
          bg-base-100 border-r border-base-300/70 shadow-2xl lg:shadow-none
          transition-transform duration-300 ease-out
          ${open ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}`}
      >
        <div className="px-5 py-6 border-b border-base-300/60">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-primary text-primary-content flex items-center justify-center shadow-lg shadow-primary/25">
              <Store size={20} />
            </div>
            <div>
              <p className="font-bold text-lg tracking-tight leading-none">
                RetailPOS
              </p>
              <p className="text-xs text-base-content/45 mt-0.5">
                Inventory & Sales
              </p>
            </div>
          </div>
        </div>

        <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-0.5">
          <p className="px-3 mb-2 text-[10px] font-semibold uppercase tracking-[0.14em] text-base-content/35">
            Menu
          </p>
          {links.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              onClick={onClose}
              className={({ isActive }) =>
                `sidebar-link flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium ${
                  isActive
                    ? "bg-primary text-primary-content shadow-md shadow-primary/20"
                    : "text-base-content/65 hover:bg-base-200 hover:text-base-content"
                }`
              }
            >
              <Icon size={18} strokeWidth={2} />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="p-4 border-t border-base-300/60 bg-base-200/30">
          <div className="flex items-center gap-3 mb-3 px-1">
            <div className="w-9 h-9 rounded-full bg-primary/15 text-primary flex items-center justify-center text-sm font-bold ring-2 ring-primary/10">
              {(user?.username || "U").slice(0, 1).toUpperCase()}
            </div>
            <div className="min-w-0 flex-1">
              <p className="text-sm font-semibold truncate">
                {user?.username || "User"}
              </p>
              <p className="text-xs text-base-content/45 capitalize">
                {user?.role || "role"}
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={logout}
            className="btn btn-ghost btn-sm w-full justify-start gap-2 text-error/80 hover:bg-error/10 hover:text-error rounded-xl"
          >
            <LogOut size={16} />
            Sign out
          </button>
        </div>
      </aside>
    </>
  );
}