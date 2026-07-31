// API helpers for analytics and scan history data.
import apiClient from "./apiClient.js";

export async function fetchAnalyticsSummary() {
  const response = await apiClient.get("/api/analytics/summary");
  return response.data;
}

export async function fetchScanHistory() {
  const response = await apiClient.get("/api/logs");
  return response.data;
}

