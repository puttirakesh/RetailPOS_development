import { useQuery } from "@tanstack/react-query";
import { Activity, CheckCircle2, XCircle } from "lucide-react";

async function fetchHealth() {
  const res = await fetch("/health");
  if (!res.ok) throw new Error("Health check failed");
  return res.json();
}

async function fetchReady() {
  const res = await fetch("/ready");
  if (!res.ok) throw new Error("Ready check failed");
  return res.json();
}

export default function App() {
  const health = useQuery({ queryKey: ["health"], queryFn: fetchHealth });
  const ready = useQuery({ queryKey: ["ready"], queryFn: fetchReady });

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-8 gap-8">
      <div className="text-center space-y-2">
        <h1 className="text-4xl font-bold tracking-tight text-primary">
          RetailPOS
        </h1>
        <p className="text-base-content/60">
          Phase 1 skeleton — backend connectivity check
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full max-w-2xl">
        <div className="card bg-base-100 shadow-sm border border-base-300">
          <div className="card-body">
            <div className="flex items-center gap-3">
              <Activity className="w-5 h-5 text-primary" />
              <h2 className="card-title text-lg">API Liveness</h2>
            </div>
            {health.isLoading && (
              <span className="loading loading-spinner loading-sm" />
            )}
            {health.isError && (
              <div className="flex items-center gap-2 text-error">
                <XCircle className="w-4 h-4" />
                <span>Unreachable — is the backend running on :8000?</span>
              </div>
            )}
            {health.data && (
              <div className="flex items-center gap-2 text-success">
                <CheckCircle2 className="w-4 h-4" />
                <span>
                  {health.data.status} — {health.data.service}
                </span>
              </div>
            )}
          </div>
        </div>

        <div className="card bg-base-100 shadow-sm border border-base-300">
          <div className="card-body">
            <div className="flex items-center gap-3">
              <Activity className="w-5 h-5 text-primary" />
              <h2 className="card-title text-lg">Database Ready</h2>
            </div>
            {ready.isLoading && (
              <span className="loading loading-spinner loading-sm" />
            )}
            {ready.isError && (
              <div className="flex items-center gap-2 text-error">
                <XCircle className="w-4 h-4" />
                <span>Unreachable</span>
              </div>
            )}
            {ready.data && (
              <div
                className={`flex items-center gap-2 ${
                  ready.data.database ? "text-success" : "text-warning"
                }`}
              >
                {ready.data.database ? (
                  <CheckCircle2 className="w-4 h-4" />
                ) : (
                  <XCircle className="w-4 h-4" />
                )}
                <span>
                  {ready.data.status}
                  {ready.data.database === false && " (DB not reachable)"}
                </span>
              </div>
            )}
          </div>
        </div>
      </div>

      <p className="text-sm text-base-content/50">
        Backend expected at{" "}
        <code className="bg-base-300 px-1 rounded">http://localhost:8000</code>
      </p>
    </div>
  );
}