import api from "./client";

export async function listCustomers({
  search = "",
  skip = 0,
  limit = 50,
  active_only = true,
} = {}) {
  const { data } = await api.get("/customers", {
    params: { search: search || undefined, skip, limit, active_only },
  });
  return data;
}

export async function createCustomer(body) {
  const { data } = await api.post("/customers", body);
  return data;
}

export async function updateCustomer(id, body) {
  const { data } = await api.put(`/customers/${id}`, body);
  return data;
}

export async function deleteCustomer(id) {
  const { data } = await api.delete(`/customers/${id}`);
  return data;
}