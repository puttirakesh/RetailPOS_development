import { Link } from "react-router-dom";
import { Tags, Package, Users, Truck, ArrowRight } from "lucide-react";
import { useAuth } from "../context/AuthContext";

const cards = [
  {
    to: "/masters/brands",
    title: "Brands",
    desc: "Product brands & margins",
    icon: Tags,
    color: "text-primary bg-primary/10",
  },
  {
    to: "/masters/products",
    title: "Products",
    desc: "Catalog & HSN codes",
    icon: Package,
    color: "text-secondary bg-secondary/10",
  },
  {
    to: "/masters/customers",
    title: "Customers",
    desc: "Credit limits & GST",
    icon: Users,
    color: "text-accent bg-accent/10",
  },
  {
    to: "/masters/suppliers",
    title: "Suppliers",
    desc: "Purchase parties",
    icon: Truck,
    color: "text-info bg-info/10",
  },
];

export default function Dashboard() {
  const { user } = useAuth();

  return (
    <div className="space-y-6">
      <div className="card-premium p-6 lg:p-8 bg-gradient-to-br from-primary/12 via-base-100 to-base-100 overflow-hidden relative">
        <div className="absolute -right-8 -top-8 w-40 h-40 rounded-full bg-primary/5 blur-2xl pointer-events-none" />
        <p className="text-sm text-base-content/55 relative">Signed in as</p>
        <h2 className="text-2xl lg:text-3xl font-bold tracking-tight mt-1 relative">
          Hello, {user?.username || "User"}
        </h2>
        <p className="text-base-content/60 mt-2 max-w-xl text-sm relative">
          Manage masters, inventory, and sales from one workspace. Start with
          Brands or open Products when ready.
        </p>
      </div>

      <div className="grid sm:grid-cols-2 xl:grid-cols-4 gap-4">
        {cards.map(({ to, title, desc, icon: Icon, color }) => (
          <Link
            key={to}
            to={to}
            className="card-premium p-5 hover:border-primary/25 group"
          >
            <div
              className={`w-10 h-10 rounded-xl flex items-center justify-center mb-3 ${color}`}
            >
              <Icon size={20} />
            </div>
            <div className="flex items-start justify-between gap-2">
              <div>
                <h3 className="font-semibold">{title}</h3>
                <p className="text-xs text-base-content/50 mt-0.5">{desc}</p>
              </div>
              <ArrowRight
                size={16}
                className="opacity-0 -translate-x-1 group-hover:opacity-50 group-hover:translate-x-0 transition-all mt-1 shrink-0"
              />
            </div>
          </Link>
        ))}
      </div>

      <div className="stats stats-vertical lg:stats-horizontal shadow-sm bg-base-100 border border-base-300/60 w-full rounded-2xl">
        <div className="stat">
          <div className="stat-title">API</div>
          <div className="stat-value text-2xl text-success">Live</div>
          <div className="stat-desc">Proxied to :8000</div>
        </div>
        <div className="stat">
          <div className="stat-title">Role</div>
          <div className="stat-value text-2xl capitalize">
            {user?.role || "—"}
          </div>
          <div className="stat-desc">JWT session</div>
        </div>
        <div className="stat">
          <div className="stat-title">Phase</div>
          <div className="stat-value text-2xl">9</div>
          <div className="stat-desc">Frontend shell</div>
        </div>
      </div>
    </div>
  );
}