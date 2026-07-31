// Custom hook that manages URL scanner form state and prediction requests.
import { useState } from "react";
import { predictUrl } from "../services/detectionService.js";

export function useUrlScanner() {
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function scanUrl() {
    setError("");
    setLoading(true);
    try {
      const data = await predictUrl(url);
      setResult(data);
    } catch (requestError) {
      setError(requestError.response?.data?.detail || "Unable to scan this URL.");
    } finally {
      setLoading(false);
    }
  }

  return { url, setUrl, result, error, loading, scanUrl };
}

