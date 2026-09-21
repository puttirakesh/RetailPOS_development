import api from "./client";

export async function listUoms({ search = "", skip = 0, limit = 100, active_only = true } = {}) {
  const { data } = await api.get("/uoms", {
    params: { search: search || undefined, skip, limit, active_only },
  });
  return data;
}

export async function createUom(body) {
  const { data } = await api.post("/uoms", body);
  return data;
}

export async function updateUom(id, body) {
  const { data } = await api.put(`/uoms/${id}`, body);
  return data;
}

export async function deleteUom(id) {
  const { data } = await api.delete(`/uoms/${id}`);
  return data;
}