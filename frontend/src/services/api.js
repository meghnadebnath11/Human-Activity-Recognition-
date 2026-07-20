const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

async function handleResponse(response) {
  const payload = await response.json();

  if (!response.ok) {
    throw new Error(payload.detail || "Request failed.");
  }

  return payload;
}

export async function fetchMetadata() {
  const response = await fetch(`${API_BASE_URL}/metadata`);
  return handleResponse(response);
}

export async function submitPrediction(payload) {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  return handleResponse(response);
}

