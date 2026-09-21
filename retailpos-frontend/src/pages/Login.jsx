import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { Store, Eye, EyeOff, AlertCircle } from "lucide-react";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("");
  const [showPw, setShowPw] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(username.trim(), password);
      navigate("/", { replace: true });
    } catch (err) {
      const detail =
        err.response?.data?.detail ||
        err.message ||
        "Login failed. Check credentials and backend.";
      setError(typeof detail === "string" ? detail : "Login failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex bg-base-200">
      <div className="hidden lg:flex lg:w-[46%] relative overflow-hidden bg-primary text-primary-content">
        <div className="absolute -top-24 -left-24 w-96 h-96 rounded-full bg-white/10 blur-3xl" />
        <div className="absolute bottom-0 right-0 w-80 h-80 rounded-full bg-white/5 blur-2xl" />
        <div className="relative z-10 flex flex-col justify-between p-12 w-full">
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-xl bg-white/20 flex items-center justify-center backdrop-blur shadow-lg">
              <Store size={22} />
            </div>
            <span className="text-xl font-bold tracking-tight">RetailPOS</span>
          </div>
          <div className="page-enter">
            <h2 className="text-4xl font-bold leading-tight tracking-tight max-w-md">
              Modern retail operations, one place.
            </h2>
            <p className="mt-4 text-primary-content/80 max-w-sm text-sm leading-relaxed">
              Inventory, masters, and sales — connected to your SQL Server RTGW
              database with secure JWT access.
            </p>
          </div>
          <p className="text-xs text-primary-content/45">
            © {new Date().getFullYear()} RetailPOS
          </p>
        </div>
      </div>

      <div className="flex-1 flex items-center justify-center p-6">
        <div className="w-full max-w-md page-enter">
          <div className="lg:hidden flex items-center gap-2 mb-8 justify-center">
            <Store className="text-primary" size={28} />
            <span className="text-xl font-bold">RetailPOS</span>
          </div>

          <div className="card-premium p-8 shadow-xl shadow-base-300/40">
            <h1 className="text-2xl font-bold tracking-tight">Welcome back</h1>
            <p className="text-sm text-base-content/55 mt-1 mb-6">
              Sign in to continue to your workspace
            </p>

            {error && (
              <div className="alert alert-error mb-4 text-sm py-3 rounded-xl">
                <AlertCircle size={18} />
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="form-control">
                <label className="label py-1">
                  <span className="label-text font-medium text-sm">
                    Username
                  </span>
                </label>
                <input
                  type="text"
                  className="input input-bordered w-full focus:input-primary rounded-xl"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  autoComplete="username"
                  required
                />
              </div>

              <div className="form-control">
                <label className="label py-1">
                  <span className="label-text font-medium text-sm">
                    Password
                  </span>
                </label>
                <div className="relative">
                  <input
                    type={showPw ? "text" : "password"}
                    className="input input-bordered w-full pr-12 focus:input-primary rounded-xl"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    autoComplete="current-password"
                    required
                  />
                  <button
                    type="button"
                    className="btn btn-ghost btn-sm btn-square absolute right-1 top-1/2 -translate-y-1/2"
                    onClick={() => setShowPw((v) => !v)}
                    tabIndex={-1}
                  >
                    {showPw ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                className="btn btn-primary w-full mt-2 rounded-xl shadow-md shadow-primary/20"
                disabled={loading}
              >
                {loading ? (
                  <span className="loading loading-spinner loading-sm" />
                ) : (
                  "Sign in"
                )}
              </button>
            </form>
          </div>

          <p className="text-center text-xs text-base-content/40 mt-6">
            Backend: <code className="opacity-70">localhost:8000</code> · Vite
            proxy
          </p>
        </div>
      </div>
    </div>
  );
}