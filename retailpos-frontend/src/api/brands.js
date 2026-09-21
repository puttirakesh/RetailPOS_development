import api from "./client";

export async function listBrands({
  search = "",
  skip = 0,
  limit = 50,
  active_only = true,
} = {}) {
  const { data } = await api.get("/brands", {
    params: {
      search: search || undefined,
      skip,
      limit,
      active_only,
    },
  });
  return data;
}

export async function createBrand(body) {
  const { data } = await api.post("/brands", body);
  return data;
}

export async function updateBrand(id, body) {
  const { data } = await api.put(`/brands/${id}`, body);
  return data;
}

export async function deleteBrand(id) {
  const { data } = await api.delete(`/brands/${id}`);
  return data;
}