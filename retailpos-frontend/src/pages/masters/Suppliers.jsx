import { useCallback, useEffect, useState } from "react";
import { Plus, Search, RefreshCw, Pencil, Trash2, X } from "lucide-react";
import {
  listSuppliers,
  createSupplier,
  updateSupplier,
  deleteSupplier,
} from "../../api/suppliers";
import LoadingBlock from "../../components/LoadingBlock";
import EmptyState from "../../components/EmptyState";

export default function Suppliers() {
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [toast, setToast] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState({
    supplier_code: "",
    supplier_name: "",
    mobile_no: "",
    address: "",
    city_id: "",
    state_id: "",
    gst_no: "",
  });
  const [saving, setSaving] = useState(false);

  const load = useCallback(async (q = search) => {
    setLoading(true);
    setError("");
    try {
      const data = await listSuppliers({ search: q, limit: 100 });
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

  async function handleSave(e) {
    e.preventDefault();
    setSaving(true);
    try {
      const body = {
        supplier_code: form.supplier_code || undefined,
        supplier_name: form.supplier_name,
        mobile_no: form.mobile_no || null,
        address: form.address || null,
        city_id: form.city_id ? Number(form.city_id) : null,
        state_id: form.state_id ? Number(form.state_id) : null,
        gst_no: form.gst_no || "",
      };
      if (editing) {
        await updateSupplier(editing.supplier_id, body);
        showToast("Updated");
      } else {
        await createSupplier(body);
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
    if (!confirm(`Delete supplier "${row.supplier_name}"?`)) return;
    try {
      await deleteSupplier(row.supplier_id);
      showToast("Deleted");
      await load();
    } catch (err) {
      showToast(err.response?.data?.detail || "Failed");
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-2 justify-between items-center">
        <p className="text-sm text-base-content/50">{total} suppliers</p>
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
              setForm({
                supplier_code: "",
                supplier_name: "",
                mobile_no: "",
                address: "",
                city_id: "",
                state_id: "",
                gst_no: "",
              });
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
          <EmptyState title="No suppliers" />
        ) : (
          <div className="overflow-x-auto">
            <table className="table table-sm">
              <thead>
                <tr className="bg-base-200/50 text-xs uppercase">
                  <th>ID</th>
                  <th>Name</th>
                  <th>Mobile</th>
                  <th>GST</th>
                  <th className="text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {items.map((row) => (
                  <tr key={row.supplier_id} className="hover">
                    <td className="font-mono text-xs opacity-60">{row.supplier_id}</td>
                    <td className="font-medium">{row.supplier_name}</td>
                    <td>{row.mobile_no || "—"}</td>
                    <td className="font-mono text-xs">{row.gst_no || "—"}</td>
                    <td className="text-right">
                      <button
                        type="button"
                        className="btn btn-ghost btn-xs"
                        onClick={() => {
                          setEditing(row);
                          setForm({
                            supplier_code: row.supplier_code || "",
                            supplier_name: row.supplier_name || "",
                            mobile_no: row.mobile_no || "",
                            address: row.address || "",
                            city_id: row.city_id != null ? String(row.city_id) : "",
                            state_id: row.state_id != null ? String(row.state_id) : "",
                            gst_no: row.gst_no || "",
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
            <h3 className="font-bold text-lg mb-4">{editing ? "Edit" : "New"} supplier</h3>
            <form onSubmit={handleSave} className="space-y-3">
              <input
                className="input input-bordered input-sm w-full"
                placeholder="Name *"
                value={form.supplier_name}
                onChange={(e) => setForm((f) => ({ ...f, supplier_name: e.target.value }))}
                required
              />
              <input
                className="input input-bordered input-sm w-full"
                placeholder="Code"
                value={form.supplier_code}
                onChange={(e) => setForm((f) => ({ ...f, supplier_code: e.target.value }))}
              />
              <input
                className="input input-bordered input-sm w-full"
                placeholder="Mobile"
                value={form.mobile_no}
                onChange={(e) => setForm((f) => ({ ...f, mobile_no: e.target.value }))}
              />
              <input
                className="input input-bordered input-sm w-full"
                placeholder="GST No"
                value={form.gst_no}
                onChange={(e) => setForm((f) => ({ ...f, gst_no: e.target.value }))}
              />
              <input
                className="input input-bordered input-sm w-full"
                placeholder="Address"
                value={form.address}
                onChange={(e) => setForm((f) => ({ ...f, address: e.target.value }))}
              />
              <div className="modal-action">
                <button type="button" className="btn btn-ghost btn-sm" onClick={() => setModalOpen(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary btn-sm rounded-xl" disabled={saving}>
                  Save
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
          <div className="alert alert-info text-sm py-2"><span>{toast}</span></div>
        </div>
      )}
    </div>
  );
}