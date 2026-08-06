// During local development Vite proxies this path to
// http://127.0.0.1:8000/api/v1, avoiding browser CORS issues.
const API_URL = import.meta.env.VITE_API_URL ?? "/api/v1";

export async function assessText(text) {
  const response = await fetch(`${API_URL}/assessments`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text })
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail ?? "The assessment could not be completed.");
  }

  return response.json();
}

export async function fetchAnalysisHistory() {
  const response = await fetch(`${API_URL}/assessments/history`);

  if (!response.ok) {
    throw new Error("Saved analyses could not be loaded.");
  }

  return response.json();
}
