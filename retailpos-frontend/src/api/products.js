import api from "./client";

export async function listProducts({
  search = "",
  category_id,
  skip = 0,
  limit = 50,
  active_only = true,
} = {}) {
  const { data } = await api.get("/products", {
    params: {
      search: search || undefined,
      category_id: category_id || undefined,
      skip,
      limit,
      active_only,
    },
  });
  return data;
}

export async function createProduct(body) {
  const { data } = await api.post("/products", body);
  return data;
}

export async function updateProduct(id, body) {
  const { data } = await api.put(`/products/${id}`, body);
  return data;
}

export async function deleteProduct(id) {
  const { data } = await api.delete(`/products/${id}`);
  return data;
}