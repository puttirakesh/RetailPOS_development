import api from "./client";

export async function listCategories({
  search = "",
  group_id,
  skip = 0,
  limit = 200,
  active_only = true,
} = {}) {
  const { data } = await api.get("/categories", {
    params: {
      search: search || undefined,
      group_id: group_id || undefined,
      skip,
      limit,
      active_only,
    },
  });
  return data;
}

export async function createCategory(body) {
  const { data } = await api.post("/categories", body);
  return data;
}

export async function updateCategory(id, body) {
  const { data } = await api.put(`/categories/${id}`, body);
  return data;
}

export async function deleteCategory(id) {
  const { data } = await api.delete(`/categories/${id}`);
  return data;
}