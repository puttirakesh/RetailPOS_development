import api from "./client";

export async function listStates({ search = "", skip = 0, limit = 100, active_only = true } = {}) {
  const { data } = await api.get("/states", {
    params: { search: search || undefined, skip, limit, active_only },
  });
  return data;
}