const API_BASE = import.meta.env.VITE_API_URL; // ex: "http://localhost:8000"

export async function apiFetch<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = localStorage.getItem("token");

  const headers: HeadersInit = {
    ...(options.headers instanceof Headers
      ? Object.fromEntries(options.headers.entries())
      : options.headers || {}),
  };

  if (!headers["Content-Type"] && !(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  let responseBody;
  try {
    responseBody = await res.json();
  } catch {
    responseBody = null;
  }

  if (!res.ok) {
    throw new Error(
      responseBody?.detail || res.statusText || "Une erreur est survenue"
    );
  }

  return responseBody;
}
export async function getConversations() {
  return await apiFetch("/chat/conversations");
}