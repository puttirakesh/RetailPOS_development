import { useCallback, useEffect, useState } from "react";
import { Plus, Search, RefreshCw, Pencil, Trash2, X } from "lucide-react";
import {
  listBrands,
  createBrand,
  updateBrand,
  deleteBrand,
} from "../../api/brands";
import LoadingBlock from "../../components/LoadingBlock";
import EmptyState from "../../components/EmptyState";

const emptyForm = {
  brand_code: "",
  brand_name: "",
  margin_percentage: 0,
  is_active: true,
};

export default function Brands() {
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [toast, setToast] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(emptyForm);
  const [saving, setSaving] = useState(false);

  const load = useCallback(
    async (q = search) => {
      setLoading(true);
      setError("");
      try {
        const data = await listBrands({ search: q, limit: 100 });
        setItems(data.items || []);
        setTotal(data.total ?? data.items?.length ?? 0);
      } catch (err) {
        setError(
          err.response?.data?.detail || err.message || "Failed to load brands"
        );
        setItems([]);
      } finally {
        setLoading(false);
      }
    },
    [search]
  );

  useEffect(() => {
    load("");
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function showToast(msg) {
    setToast(msg);
    setTimeout(() => setToast(""), 2800);
  }

  function openCreate() {
    setEditing(null);
    setForm(emptyForm);
    setModalOpen(true);
  }

  function openEdit(row) {
    setEditing(row);
    setForm({
      brand_code: row.brand_code || "",
      brand_name: row.brand_name || "",
      margin_percentage: row.margin_percentage ?? 0,
      is_active: row.is_active !== false,
    });
    setModalOpen(true);
  }

  async function handleSave(e) {
    e.preventDefault();
    setSaving(true);
    try {
      const body = {
        brand_code: form.brand_code || undefined,
        brand_name: form.brand_name,
        margin_percentage: Number(form.margin_percentage) || 0,
        is_active: form.is_active,
      };
      if (editing) {
        await updateBrand(editing.brand_id, body);
        showToast("Brand updated");
      } else {
        await createBrand(body);
        showToast("Brand created");
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
    if (!confirm(`Deactivate brand "${row.brand_name}"?`)) return;
    try {
      await deleteBrand(row.brand_id);
      showToast("Brand deactivated");
      await load();
    } catch (err) {
      showToast(err.response?.data?.detail || "Delete failed");
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row gap-3 sm:items-center sm:justify-between">
        <p className="text-sm text-base-content/50">
          {total} brand{total === 1 ? "" : "s"}
        </p>
        <div className="flex flex-wrap gap-2">
          <label className="input input-bordered input-sm flex items-center gap-2 min-w-[200px] bg-base-100">
            <Search size={14} className="opacity-50" />
            <input
              type="search"
              placeholder="Search brands…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && load(search)}
            />
          </label>
          <button
            type="button"
            className="btn btn-ghost btn-sm"
            onClick={() => load()}
            title="Refresh"
          >
            <RefreshCw size={16} />
          </button>
          <button
            type="button"
            className="btn btn-primary btn-sm gap-1"
            onClick={openCreate}
          >
            <Plus size={16} />
            Add brand
          </button>
        </div>
      </div>

      <div className="card-premium overflow-hidden">
        {loading ? (
          <LoadingBlock label="Loading brands…" />
        ) : error ? (
          <div className="p-6">
            <div className="alert alert-error text-sm">
              <span>{error}</span>
              <button type="button" className="btn btn-sm" onClick={() => load()}>
                Retry
              </button>
            </div>
          </div>
        ) : items.length === 0 ? (
          <EmptyState
            title="No brands found"
            hint="Try a different search or add a new brand."
          />
        ) : (
          <div className="overflow-x-auto">
            <table className="table table-sm">
              <thead>
                <tr className="bg-base-200/50 text-xs uppercase tracking-wide">
                  <th className="font-semibold">ID</th>
                  <th className="font-semibold">Code</th>
                  <th className="font-semibold">Name</th>
                  <th className="font-semibold text-right">Margin %</th>
                  <th className="font-semibold">Status</th>
                  <th className="font-semibold text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {items.map((row) => (
                  <tr key={row.brand_id} className="hover">
                    <td className="font-mono text-xs opacity-60">
                      {row.brand_id}
                    </td>
                    <td className="font-medium">{row.brand_code}</td>
                    <td>{row.brand_name}</td>
                    <td className="text-right tabular-nums">
                      {Number(row.margin_percentage ?? 0).toFixed(2)}
                    </td>
                    <td>
                      <span
                        className={`badge badge-sm ${
                          row.is_active
                            ? "badge-success badge-outline"
                            : "badge-ghost"
                        }`}
                      >
                        {row.is_active ? "Active" : "Inactive"}
                      </span>
                    </td>
                    <td className="text-right">
                      <div className="join">
                        <button
                          type="button"
                          className="btn btn-ghost btn-xs join-item"
                          onClick={() => openEdit(row)}
                        >
                          <Pencil size={14} />
                        </button>
                        <button
                          type="button"
                          className="btn btn-ghost btn-xs join-item text-error"
                          onClick={() => handleDelete(row)}
                          disabled={!row.is_active}
                        >
                          <Trash2 size={14} />
                        </button>
                      </div>
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
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-lg">
                {editing ? "Edit brand" : "New brand"}
              </h3>
              <button
                type="button"
                className="btn btn-ghost btn-sm btn-square"
                onClick={() => setModalOpen(false)}
              >
                <X size={18} />
              </button>
            </div>
            <form onSubmit={handleSave} className="space-y-3">
              <div className="form-control">
                <label className="label py-0">
                  <span className="label-text text-xs font-medium">Code</span>
                </label>
                <input
                  className="input input-bordered input-sm"
                  value={form.brand_code}
                  onChange={(e) =>
                    setForm((f) => ({ ...f, brand_code: e.target.value }))
                  }
                  placeholder="Auto if empty"
                />
              </div>
              <div className="form-control">
                <label className="label py-0">
                  <span className="label-text text-xs font-medium">Name *</span>
                </label>
                <input
                  className="input input-bordered input-sm"
                  value={form.brand_name}
                  onChange={(e) =>
                    setForm((f) => ({ ...f, brand_name: e.target.value }))
                  }
                  required
                />
              </div>
              <div className="form-control">
                <label className="label py-0">
                  <span className="label-text text-xs font-medium">Margin %</span>
                </label>
                <input
                  type="number"
                  step="0.01"
                  className="input input-bordered input-sm"
                  value={form.margin_percentage}
                  onChange={(e) =>
                    setForm((f) => ({
                      ...f,
                      margin_percentage: e.target.value,
                    }))
                  }
                />
              </div>
              <label className="label cursor-pointer justify-start gap-3 py-1">
                <input
                  type="checkbox"
                  className="toggle toggle-primary toggle-sm"
                  checked={form.is_active}
                  onChange={(e) =>
                    setForm((f) => ({ ...f, is_active: e.target.checked }))
                  }
                />
                <span className="label-text text-sm">Active</span>
              </label>
              <div className="modal-action mt-4">
                <button
                  type="button"
                  className="btn btn-ghost btn-sm"
                  onClick={() => setModalOpen(false)}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn btn-primary btn-sm"
                  disabled={saving}
                >
                  {saving ? (
                    <span className="loading loading-spinner loading-xs" />
                  ) : (
                    "Save"
                  )}
                </button>
              </div>
            </form>
          </div>
          <form method="dialog" className="modal-backdrop">
            <button type="button" onClick={() => setModalOpen(false)}>
              close
            </button>
          </form>
        </dialog>
      )}

      {toast && (
        <div className="toast toast-end z-50">
          <div className="alert alert-info shadow-lg text-sm py-2">
            <span>{toast}</span>
          </div>
        </div>
      )}
    </div>
  );
}