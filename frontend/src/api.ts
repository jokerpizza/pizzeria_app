export async function getCategories() {
  const res = await fetch("/api/categories/");
  return res.json();
}
export async function createCategory(data: { name: string }) {
  const res = await fetch("/api/categories/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}
export async function updateCategory(id: number, data: { name: string }) {
  const res = await fetch(`/api/categories/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}
export async function deleteCategory(id: number) {
  const res = await fetch(`/api/categories/${id}`, { method: "DELETE" });
  return res.json();
}

// --- ISTNIEJĄCE FUNKCJE PONIŻEJ ---
// export async function getRecipes() ... itd.
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL + '/api',
});

export default api;
