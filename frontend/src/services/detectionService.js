// API helpers for phishing URL prediction requests.
import apiClient from "./apiClient.js";

export async function predictUrl(url) {
  const response = await apiClient.post("/predict", { url });
  return response.data;
}

