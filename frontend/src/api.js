// Tiny fetch wrapper: adds the auth token and turns errors into exceptions.
export const getToken = () => localStorage.getItem("token");

export async function api(path, { method = "GET", body } = {}) {
  const res = await fetch(`/api/${path}`, {
    method,
    headers: {
      "Content-Type": "application/json",
      ...(getToken() ? { Authorization: `Token ${getToken()}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (res.status === 204) return null;
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(data.detail || "Something went wrong.");
    err.status = res.status;
    throw err;
  }
  return data;
}
