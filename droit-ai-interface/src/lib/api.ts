
/**
 * api.ts
 *
 * Fournit une fonction utilitaire `apiFetch` pour effectuer des appels HTTP 
 * vers l'API backend avec gestion automatique du token JWT et des en-têtes.
 *
 * Fonctions principales :
 * - `apiFetch<T>(path, options)`: appel typé à l'API, avec gestion du token et des erreurs.
 * - `getConversations()`: raccourci pour récupérer les conversations utilisateur.
 *
 * Caractéristiques :
 * - Utilise `import.meta.env.VITE_API_URL` comme base d'URL.
 * - Supporte automatiquement les en-têtes `Authorization` et `Content-Type`.
 * - Gère proprement les erreurs HTTP avec message personnalisé.
 *
 * Auteur : Clément Gardair  
 * Projet : PROJET-DROIT-IA-V2
 */


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