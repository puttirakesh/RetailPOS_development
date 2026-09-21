import { useCallback, useEffect, useState } from "react";
import { Plus, Search, RefreshCw, Pencil, Trash2, X } from "lucide-react";
import {
  listCustomers,
  createCustomer,
  updateCustomer,
  deleteCustomer,
} from "../../api/customers";
import { listStates } from "../../api/states";
import LoadingBlock from "../../components/LoadingBlock";
import EmptyState from "../../components/EmptyState";

const emptyForm = {
  customer_code: "",
  customer_name: "",
  mobile_no: "",
  address: "",
  city_id: "",
  state_id: "",
  gst_no: "",
  credit_days: 0,
  credit_limit: 0,
  opening_balance: 0,
  ledger_required: false,
  email_id: "",
  is_active: true,
};

export default function Customers() {
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [states, setStates] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [toast, setToast] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(emptyForm);
  const [saving, setSaving] = useState(false);

  const load = useCallback(async (q = search) => {
    setLoading(true);
    setError("");
    try {
      const data = await listCustomers({ search: q, limit: 100 });
      setItems(data.items || []);
      setTotal(data.total ?? data.items?.length ?? 0);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "Failed to load");
      setItems([]);
    } finally {
      setLoading(false);
    }
  }, [search]);

  useEffect(() => {
    listStates({ limit: 100 }).then((d) => setStates(d.items || [])).catch(() => {});
    load("");
  }, []);

  function showToast(msg) {
    setToast(String(msg));
    setTimeout(() => setToast(""), 2800);
  }

  function openCreate() {
    setEditing(null);
    setForm({
      ...emptyForm,
      state_id: states[0]?.state_id ? String(states[0].state_id) : "",
    });
    setModalOpen(true);
  }

  function openEdit(row) {
    setEditing(row);
    setForm({
      customer_code: row.customer_code || "",
      customer_name: row.customer_name || "",
      mobile_no: row.mobile_no || "",
      address: row.address || "",
      city_id: row.city_id != null ? String(row.city_id) : "",
      state_id: row.state_id ? String(row.state_id) : "",
      gst_no: row.gst_no || "",
      credit_days: row.credit_days ?? 0,
      credit_limit: row.credit_limit ?? 0,
      opening_balance: row.opening_balance ?? 0,
      ledger_required: !!row.ledger_required,
      email_id: row.email_id || "",
      is_active: row.is_active !== false,
    });
    setModalOpen(true);
  }

  async function handleSave(e) {
    e.preventDefault();
    if (!form.state_id) {
      showToast("State is required");
      return;
    }
    setSaving(true);
    try {
      const body = {
        customer_code: form.customer_code || undefined,
        customer_name: form.customer_name,
        mobile_no: form.mobile_no || null,
        address: form.address || null,
        city_id: form.city_id ? Number(form.city_id) : null,
        state_id: Number(form.state_id),
        gst_no: form.gst_no || null,
        credit_days: Number(form.credit_days) || 0,
        credit_limit: Number(form.credit_limit) || 0,
        opening_balance: Number(form.opening_balance) || 0,
        ledger_required: form.ledger_required,
        email_id: form.email_id || null,
        is_active: form.is_active,
      };
      if (editing) {
        await updateCustomer(editing.customer_id, body);
        showToast("Customer updated");
      } else {
        await createCustomer(body);
        showToast("Customer created");
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
    if (!confirm(`Deactivate "${row.customer_name}"?`)) return;
    try {
      await deleteCustomer(row.customer_id);
      showToast("Customer deactivated");
      await load();
    } catch (err) {
      showToast(err.response?.data?.detail || "Delete failed");
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row gap-3 sm:items-center sm:justify-between">
        <p className="text-sm text-base-content/50">{total} customers</p>
        <div className="flex flex-wrap gap-2">
          <label className="input input-bordered input-sm flex items-center gap-2 min-w-[200px] bg-base-100">
            <Search size={14} className="opacity-50" />
            <input
              type="search"
              placeholder="Search…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && load(search)}
            />
          </label>
          <button type="button" className="btn btn-ghost btn-sm" onClick={() => load()}>
            <RefreshCw size={16} />
          </button>
          <button type="button" className="btn btn-primary btn-sm gap-1 rounded-xl" onClick={openCreate}>
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
          <EmptyState title="No customers" />
        ) : (
          <div className="overflow-x-auto">
            <table className="table table-sm">
              <thead>
                <tr className="bg-base-200/50 text-xs uppercase">
                  <th>ID</th>
                  <th>Name</th>
                  <th>Mobile</th>
                  <th>GST</th>
                  <th>Credit</th>
                  <th>Status</th>
                  <th className="text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {items.map((row) => (
                  <tr key={row.customer_id} className="hover">
                    <td className="font-mono text-xs opacity-60">{row.customer_id}</td>
                    <td className="font-medium">{row.customer_name}</td>
                    <td>{row.mobile_no || "—"}</td>
                    <td className="font-mono text-xs">{row.gst_no || "—"}</td>
                    <td className="tabular-nums text-xs">{Number(row.credit_limit ?? 0).toFixed(0)}</td>
                    <td>
                      <span className={`badge badge-sm ${row.is_active ? "badge-success badge-outline" : "badge-ghost"}`}>
                        {row.is_active ? "Active" : "Off"}
                      </span>
                    </td>
                    <td className="text-right">
                      <button type="button" className="btn btn-ghost btn-xs" onClick={() => openEdit(row)}>
                        <Pencil size={14} />
                      </button>
                      <button
                        type="button"
                        className="btn btn-ghost btn-xs text-error"
                        disabled={!row.is_active}
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
          <div className="modal-box max-w-lg rounded-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between mb-4">
              <h3 className="font-bold text-lg">{editing ? "Edit customer" : "New customer"}</h3>
              <button type="button" className="btn btn-ghost btn-sm btn-square" onClick={() => setModalOpen(false)}>
                <X size={18} />
              </button>
            </div>
            <form onSubmit={handleSave} className="space-y-3">
              <input
                className="input input-bordered input-sm w-full"
                placeholder="Name *"
                value={form.customer_name}
                onChange={(e) => setForm((f) => ({ ...f, customer_name: e.target.value }))}
                required
              />
              <div className="grid grid-cols-2 gap-2">
                <input
                  className="input input-bordered input-sm"
                  placeholder="Code"
                  value={form.customer_code}
                  onChange={(e) => setForm((f) => ({ ...f, customer_code: e.target.value }))}
                />
                <input
                  className="input input-bordered input-sm"
                  placeholder="Mobile"
                  value={form.mobile_no}
                  onChange={(e) => setForm((f) => ({ ...f, mobile_no: e.target.value }))}
                />
              </div>
              <select
                className="select select-bordered select-sm w-full"
                value={form.state_id}
                onChange={(e) => setForm((f) => ({ ...f, state_id: e.target.value }))}
                required
              >
                <option value="">State *</option>
                {states.map((s) => (
                  <option key={s.state_id} value={s.state_id}>
                    {s.state_name}
                  </option>
                ))}
              </select>
              <input
                className="input input-bordered input-sm w-full"
                placeholder="Address"
                value={form.address}
                onChange={(e) => setForm((f) => ({ ...f, address: e.target.value }))}
              />
              <input
                className="input input-bordered input-sm w-full"
                placeholder="GST No"
                value={form.gst_no}
                onChange={(e) => setForm((f) => ({ ...f, gst_no: e.target.value }))}
              />
              <div className="grid grid-cols-3 gap-2">
                <input
                  type="number"
                  className="input input-bordered input-sm"
                  placeholder="Credit days"
                  value={form.credit_days}
                  onChange={(e) => setForm((f) => ({ ...f, credit_days: e.target.value }))}
                />
                <input
                  type="number"
                  className="input input-bordered input-sm"
                  placeholder="Credit limit"
                  value={form.credit_limit}
                  onChange={(e) => setForm((f) => ({ ...f, credit_limit: e.target.value }))}
                />
                <input
                  type="number"
                  className="input input-bordered input-sm"
                  placeholder="Opening bal"
                  value={form.opening_balance}
                  onChange={(e) => setForm((f) => ({ ...f, opening_balance: e.target.value }))}
                />
              </div>
              <input
                className="input input-bordered input-sm w-full"
                placeholder="Email"
                value={form.email_id}
                onChange={(e) => setForm((f) => ({ ...f, email_id: e.target.value }))}
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
          <div className="alert alert-info text-sm py-2"><span>{toast}</span></div>
        </div>
      )}
    </div>
  );
}