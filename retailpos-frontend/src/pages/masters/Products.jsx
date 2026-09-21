import { useCallback, useEffect, useState } from "react";
import { Plus, Search, RefreshCw, Pencil, Trash2, X } from "lucide-react";
import {
  listProducts,
  createProduct,
  updateProduct,
  deleteProduct,
} from "../../api/products";
import { listCategories } from "../../api/categories";
import LoadingBlock from "../../components/LoadingBlock";
import EmptyState from "../../components/EmptyState";

const emptyForm = {
  product_code: "",
  product_name: "",
  category_id: "",
  hsn_code: "",
  remarks: "",
  is_unique: false,
  is_bulk: false,
  auto_ean_required: false,
  entry_wise_ean_required: false,
  discount_not_applicable: false,
  manual_barcode_restriction: false,
  non_inventory: false,
  uom_id: "",
  is_active: true,
};

export default function Products() {
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [categories, setCategories] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [toast, setToast] = useState("");
  const [modalOpen, setModalOpen] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState(emptyForm);
  const [saving, setSaving] = useState(false);

  const loadCategories = useCallback(async () => {
    try {
      const data = await listCategories({ limit: 200 });
      setCategories(data.items || []);
    } catch {
      setCategories([]);
    }
  }, []);

  const load = useCallback(
    async (q = search) => {
      setLoading(true);
      setError("");
      try {
        const data = await listProducts({ search: q, limit: 100 });
        setItems(data.items || []);
        setTotal(data.total ?? data.items?.length ?? 0);
      } catch (err) {
        setError(
          err.response?.data?.detail || err.message || "Failed to load products"
        );
        setItems([]);
      } finally {
        setLoading(false);
      }
    },
    [search]
  );

  useEffect(() => {
    loadCategories();
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
      category_id: categories[0]?.category_id
        ? String(categories[0].category_id)
        : "",
    });
    setModalOpen(true);
  }

  function openEdit(row) {
    setEditing(row);
    setForm({
      product_code: row.product_code || "",
      product_name: row.product_name || "",
      category_id: row.category_id ? String(row.category_id) : "",
      hsn_code: row.hsn_code || "",
      remarks: row.remarks || "",
      is_unique: !!row.is_unique,
      is_bulk: !!row.is_bulk,
      auto_ean_required: !!row.auto_ean_required,
      entry_wise_ean_required: !!row.entry_wise_ean_required,
      discount_not_applicable: !!row.discount_not_applicable,
      manual_barcode_restriction: !!row.manual_barcode_restriction,
      non_inventory: !!row.non_inventory,
      uom_id: row.uom_id != null ? String(row.uom_id) : "",
      is_active: row.is_active !== false,
    });
    setModalOpen(true);
  }

  function categoryName(id) {
    const c = categories.find((x) => x.category_id === id);
    return c?.category_name || id;
  }

  async function handleSave(e) {
    e.preventDefault();
    if (!form.category_id) {
      showToast("Category is required");
      return;
    }
    setSaving(true);
    try {
      const body = {
        product_code: form.product_code || undefined,
        product_name: form.product_name,
        category_id: Number(form.category_id),
        hsn_code: form.hsn_code || null,
        remarks: form.remarks || null,
        is_unique: form.is_unique,
        is_bulk: form.is_bulk,
        auto_ean_required: form.auto_ean_required,
        entry_wise_ean_required: form.entry_wise_ean_required,
        discount_not_applicable: form.discount_not_applicable,
        manual_barcode_restriction: form.manual_barcode_restriction,
        non_inventory: form.non_inventory,
        uom_id: form.uom_id ? Number(form.uom_id) : null,
        is_active: form.is_active,
      };
      if (editing) {
        await updateProduct(editing.product_id, body);
        showToast("Product updated");
      } else {
        await createProduct(body);
        showToast("Product created");
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
    if (!confirm(`Deactivate product "${row.product_name}"?`)) return;
    try {
      await deleteProduct(row.product_id);
      showToast("Product deactivated");
      await load();
    } catch (err) {
      showToast(err.response?.data?.detail || "Delete failed");
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row gap-3 sm:items-center sm:justify-between">
        <p className="text-sm text-base-content/50">
          {total} product{total === 1 ? "" : "s"}
        </p>
        <div className="flex flex-wrap gap-2">
          <label className="input input-bordered input-sm flex items-center gap-2 min-w-[200px] bg-base-100">
            <Search size={14} className="opacity-50" />
            <input
              type="search"
              placeholder="Search products…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && load(search)}
            />
          </label>
          <button type="button" className="btn btn-ghost btn-sm" onClick={() => load()}>
            <RefreshCw size={16} />
          </button>
          <button type="button" className="btn btn-primary btn-sm gap-1 rounded-xl" onClick={openCreate}>
            <Plus size={16} />
            Add product
          </button>
        </div>
      </div>

      <div className="card-premium overflow-hidden">
        {loading ? (
          <LoadingBlock label="Loading products…" />
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
          <EmptyState title="No products found" hint="Add a product or change search." />
        ) : (
          <div className="overflow-x-auto">
            <table className="table table-sm">
              <thead>
                <tr className="bg-base-200/50 text-xs uppercase tracking-wide">
                  <th>ID</th>
                  <th>Code</th>
                  <th>Name</th>
                  <th>Category</th>
                  <th>HSN</th>
                  <th>Flags</th>
                  <th>Status</th>
                  <th className="text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {items.map((row) => (
                  <tr key={row.product_id} className="hover">
                    <td className="font-mono text-xs opacity-60">{row.product_id}</td>
                    <td className="font-medium">{row.product_code}</td>
                    <td>{row.product_name}</td>
                    <td className="text-xs">{categoryName(row.category_id)}</td>
                    <td className="font-mono text-xs">{row.hsn_code || "—"}</td>
                    <td className="text-xs space-x-1">
                      {row.is_unique && <span className="badge badge-ghost badge-xs">Unique</span>}
                      {row.is_bulk && <span className="badge badge-ghost badge-xs">Bulk</span>}
                      {row.non_inventory && <span className="badge badge-ghost badge-xs">Non-inv</span>}
                    </td>
                    <td>
                      <span
                        className={`badge badge-sm ${
                          row.is_active ? "badge-success badge-outline" : "badge-ghost"
                        }`}
                      >
                        {row.is_active ? "Active" : "Inactive"}
                      </span>
                    </td>
                    <td className="text-right">
                      <div className="join">
                        <button type="button" className="btn btn-ghost btn-xs join-item" onClick={() => openEdit(row)}>
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
          <div className="modal-box max-w-lg rounded-2xl max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-lg">{editing ? "Edit product" : "New product"}</h3>
              <button type="button" className="btn btn-ghost btn-sm btn-square" onClick={() => setModalOpen(false)}>
                <X size={18} />
              </button>
            </div>
            <form onSubmit={handleSave} className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div className="form-control">
                  <label className="label py-0"><span className="label-text text-xs font-medium">Code</span></label>
                  <input
                    className="input input-bordered input-sm"
                    value={form.product_code}
                    onChange={(e) => setForm((f) => ({ ...f, product_code: e.target.value }))}
                    placeholder="Auto if empty"
                  />
                </div>
                <div className="form-control">
                  <label className="label py-0"><span className="label-text text-xs font-medium">HSN</span></label>
                  <input
                    className="input input-bordered input-sm"
                    value={form.hsn_code}
                    onChange={(e) => setForm((f) => ({ ...f, hsn_code: e.target.value }))}
                  />
                </div>
              </div>
              <div className="form-control">
                <label className="label py-0"><span className="label-text text-xs font-medium">Name *</span></label>
                <input
                  className="input input-bordered input-sm"
                  value={form.product_name}
                  onChange={(e) => setForm((f) => ({ ...f, product_name: e.target.value }))}
                  required
                />
              </div>
              <div className="form-control">
                <label className="label py-0"><span className="label-text text-xs font-medium">Category *</span></label>
                <select
                  className="select select-bordered select-sm"
                  value={form.category_id}
                  onChange={(e) => setForm((f) => ({ ...f, category_id: e.target.value }))}
                  required
                >
                  <option value="">Select category</option>
                  {categories.map((c) => (
                    <option key={c.category_id} value={c.category_id}>
                      {c.category_name} ({c.category_id})
                    </option>
                  ))}
                </select>
              </div>
              <div className="form-control">
                <label className="label py-0"><span className="label-text text-xs font-medium">Remarks</span></label>
                <input
                  className="input input-bordered input-sm"
                  value={form.remarks}
                  onChange={(e) => setForm((f) => ({ ...f, remarks: e.target.value }))}
                />
              </div>
              <div className="grid grid-cols-2 gap-2 text-sm">
                {[
                  ["is_unique", "Unique"],
                  ["is_bulk", "Bulk"],
                  ["auto_ean_required", "Auto EAN"],
                  ["entry_wise_ean_required", "Entry EAN"],
                  ["discount_not_applicable", "No discount"],
                  ["manual_barcode_restriction", "Manual barcode"],
                  ["non_inventory", "Non-inventory"],
                  ["is_active", "Active"],
                ].map(([key, label]) => (
                  <label key={key} className="label cursor-pointer justify-start gap-2 py-1">
                    <input
                      type="checkbox"
                      className="checkbox checkbox-primary checkbox-xs"
                      checked={form[key]}
                      onChange={(e) => setForm((f) => ({ ...f, [key]: e.target.checked }))}
                    />
                    <span className="label-text text-xs">{label}</span>
                  </label>
                ))}
              </div>
              <div className="modal-action mt-4">
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
          <div className="alert alert-info shadow-lg text-sm py-2">
            <span>{toast}</span>
          </div>
        </div>
      )}
    </div>
  );
}