import { useCallback, useEffect, useState } from "react";
import { Plus, Search, RefreshCw, Pencil, Trash2, X } from "lucide-react";
import { listUoms, createUom, updateUom, deleteUom } from "../../api/uoms";
import LoadingBlock from "../../components/LoadingBlock";
import EmptyState from "../../components/EmptyState";

export default function Uoms() {
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [toast, setToast] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState({ uom_code: "", uom_name: "", is_active: true });
  const [saving, setSaving] = useState(false);

  const load = useCallback(async (q = search) => {
    setLoading(true);
    setError("");
    try {
      const data = await listUoms({ search: q, limit: 100 });
      setItems(data.items || []);
      setTotal(data.total ?? data.items?.length ?? 0);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "Failed");
      setItems([]);
    } finally {
      setLoading(false);
    }
  }, [search]);

  useEffect(() => {
    load("");
  }, []);

  function showToast(msg) {
    setToast(String(msg));
    setTimeout(() => setToast(""), 2800);
  }

  // Field names may be uom_id / uom_name — match Swagger BrandRead style
  const idKey = "uom_id";
  const nameKey = "uom_name";
  const codeKey = "uom_code";

  async function handleSave(e) {
    e.preventDefault();
    setSaving(true);
    try {
      const body = {
        [codeKey]: form.uom_code || undefined,
        [nameKey]: form.uom_name,
        is_active: form.is_active,
      };
      if (editing) {
        await updateUom(editing[idKey], body);
        showToast("Updated");
      } else {
        await createUom(body);
        showToast("Created");
      }
      setModalOpen(false);
      await load();
    } catch (err) {
      showToast(err.response?.data?.detail || "Save failed");
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(row) {
    if (!confirm(`Deactivate "${row[nameKey]}"?`)) return;
    try {
      await deleteUom(row[idKey]);
      showToast("Deactivated");
      await load();
    } catch (err) {
      showToast(err.response?.data?.detail || "Failed");
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-2 justify-between items-center">
        <p className="text-sm text-base-content/50">{total} UOMs</p>
        <div className="flex gap-2">
          <label className="input input-bordered input-sm flex items-center gap-2 bg-base-100">
            <Search size={14} className="opacity-50" />
            <input
              type="search"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && load(search)}
              placeholder="Search…"
            />
          </label>
          <button type="button" className="btn btn-ghost btn-sm" onClick={() => load()}>
            <RefreshCw size={16} />
          </button>
          <button
            type="button"
            className="btn btn-primary btn-sm gap-1 rounded-xl"
            onClick={() => {
              setEditing(null);
              setForm({ uom_code: "", uom_name: "", is_active: true });
              setModalOpen(true);
            }}
          >
            <Plus size={16} /> Add
          </button>
        </div>
      </div>

      <div className="card-premium overflow-hidden">
        {loading ? (
          <LoadingBlock />
        ) : error ? (
          <div className="p-6 alert alert-error text-sm">{error}</div>
        ) : items.length === 0 ? (
          <EmptyState title="No UOMs" />
        ) : (
          <div className="overflow-x-auto">
            <table className="table table-sm">
              <thead>
                <tr className="bg-base-200/50 text-xs uppercase">
                  <th>ID</th>
                  <th>Code</th>
                  <th>Name</th>
                  <th>Status</th>
                  <th className="text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {items.map((row) => (
                  <tr key={row[idKey]} className="hover">
                    <td className="font-mono text-xs opacity-60">{row[idKey]}</td>
                    <td>{row[codeKey]}</td>
                    <td className="font-medium">{row[nameKey]}</td>
                    <td>
                      <span
                        className={`badge badge-sm ${
                          row.is_active !== false
                            ? "badge-success badge-outline"
                            : "badge-ghost"
                        }`}
                      >
                        {row.is_active !== false ? "Active" : "Off"}
                      </span>
                    </td>
                    <td className="text-right">
                      <button
                        type="button"
                        className="btn btn-ghost btn-xs"
                        onClick={() => {
                          setEditing(row);
                          setForm({
                            uom_code: row[codeKey] || "",
                            uom_name: row[nameKey] || "",
                            is_active: row.is_active !== false,
                          });
                          setModalOpen(true);
                        }}
                      >
                        <Pencil size={14} />
                      </button>
                      <button
                        type="button"
                        className="btn btn-ghost btn-xs text-error"
                        onClick={() => handleDelete(row)}
                      >
                        <Trash2 size={14} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {modalOpen && (
        <dialog className="modal modal-open">
          <div className="modal-box max-w-md rounded-2xl">
            <h3 className="font-bold text-lg mb-4">{editing ? "Edit" : "New"} UOM</h3>
            <form onSubmit={handleSave} className="space-y-3">
              <input
                className="input input-bordered input-sm w-full"
                placeholder="Code"
                value={form.uom_code}
                onChange={(e) => setForm((f) => ({ ...f, uom_code: e.target.value }))}
              />
              <input
                className="input input-bordered input-sm w-full"
                placeholder="Name *"
                value={form.uom_name}
                onChange={(e) => setForm((f) => ({ ...f, uom_name: e.target.value }))}
                required
              />
              <label className="label cursor-pointer justify-start gap-2">
                <input
                  type="checkbox"
                  className="toggle toggle-primary toggle-sm"
                  checked={form.is_active}
                  onChange={(e) => setForm((f) => ({ ...f, is_active: e.target.checked }))}
                />
                <span className="label-text text-sm">Active</span>
              </label>
              <div className="modal-action">
                <button type="button" className="btn btn-ghost btn-sm" onClick={() => setModalOpen(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary btn-sm rounded-xl" disabled={saving}>
                  {saving ? <span className="loading loading-spinner loading-xs" /> : "Save"}
                </button>
              </div>
            </form>
          </div>
          <form method="dialog" className="modal-backdrop">
            <button type="button" onClick={() => setModalOpen(false)}>close</button>
          </form>
        </dialog>
      )}

      {toast && (
        <div className="toast toast-end z-50">
          <div className="alert alert-info text-sm py-2">
            <span>{toast}</span>
          </div>
        </div>
      )}
    </div>
  );
}