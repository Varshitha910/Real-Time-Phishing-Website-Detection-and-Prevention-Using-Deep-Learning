"""Load the trained phishing model and run real-time inference."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse

import joblib
import numpy as np
import tensorflow as tf

from backend.ml.feature_extraction import FEATURE_COLUMNS, extract_url_features, feature_vector, sanitize_url


PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ML_DIR = PROJECT_ROOT / "backend" / "ml"
ROOT_ARTIFACTS_DIR = PROJECT_ROOT / "ml" / "artifacts"

MODEL_CANDIDATES = [
    BACKEND_ML_DIR / "model.h5",
    ROOT_ARTIFACTS_DIR / "phishing_model.keras",
]

SCALER_CANDIDATES = [
    BACKEND_ML_DIR / "scaler.pkl",
    ROOT_ARTIFACTS_DIR / "scaler.pkl",
]


class MLPhishingModel:
    """Artifact-backed predictor for phishing URL classification."""

    def __init__(self) -> None:
        self.model_path = _first_existing(MODEL_CANDIDATES, "model")
        self.scaler_path = _first_existing(SCALER_CANDIDATES, "scaler")
        self.model = tf.keras.models.load_model(self.model_path)
        self.scaler = joblib.load(self.scaler_path)

    def predict(self, url: str) -> dict[str, object]:
        """Return model prediction, confidence, risk, and extracted features."""

        normalized_url = sanitize_url(url)
        _validate_url(normalized_url)

        features = extract_url_features(normalized_url)
        vector = np.array([feature_vector(normalized_url)], dtype=float)
        scaled_vector = self.scaler.transform(vector)
        phishing_probability = float(self.model.predict(scaled_vector, verbose=0).ravel()[0])

        prediction = "Phishing" if phishing_probability >= 0.5 else "Legitimate"
        confidence = phishing_probability if prediction == "Phishing" else 1.0 - phishing_probability
        risk_level = _risk_level(phishing_probability)

        return {
            "url": normalized_url,
            "prediction": prediction,
            "confidence": round(confidence * 100, 2),
            "risk_level": risk_level,
            "phishing_probability": round(phishing_probability, 6),
            "features": features,
            "feature_columns": FEATURE_COLUMNS,
        }


@lru_cache(maxsize=1)
def get_model() -> MLPhishingModel:
    """Cache the loaded model so every request does not reload artifacts."""

    return MLPhishingModel()


def predict_url(url: str) -> dict[str, object]:
    """Convenience function for FastAPI routes and services."""

    return get_model().predict(url)


def _first_existing(paths: list[Path], artifact_name: str) -> Path:
    """Return the first existing artifact path or fail with a clear message."""

    for path in paths:
        if path.exists():
            return path
    searched = ", ".join(str(path) for path in paths)
    raise FileNotFoundError(f"No trained {artifact_name} artifact found. Searched: {searched}")


def _validate_url(url: str) -> None:
    """Validate normalized HTTP/HTTPS URLs."""

    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Invalid URL. Provide a valid http:// or https:// URL.")


def _risk_level(phishing_probability: float) -> str:
    """Convert phishing probability to Low, Medium, High, or Critical."""

    if phishing_probability >= 0.9:
        return "Critical"
    if phishing_probability >= 0.75:
        return "High"
    if phishing_probability >= 0.4:
        return "Medium"
    return "Low"

