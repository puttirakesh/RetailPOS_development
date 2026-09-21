import api from "./client";

export async function listSuppliers({ search = "", skip = 0, limit = 50 } = {}) {
  const { data } = await api.get("/suppliers", {
    params: { search: search || undefined, skip, limit },
  });
  return data;
}

export async function createSupplier(body) {
  const { data } = await api.post("/suppliers", body);
  return data;
}

export async function updateSupplier(id, body) {
  const { data } = await api.put(`/suppliers/${id}`, body);
  return data;
}

export async function deleteSupplier(id) {
  const { data } = await api.delete(`/suppliers/${id}`);
  return data;
}