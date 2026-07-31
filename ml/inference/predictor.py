"""Production inference wrapper for phishing URL prediction.

This module loads the trained Keras model and fitted StandardScaler from
ml/artifacts, accepts a raw URL, extracts the same numerical features used
during training, scales them, and returns a user-facing prediction response.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import joblib
import numpy as np
import tensorflow as tf

from ml.feature_extraction.url_features import FEATURE_COLUMNS, extract_features


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = PROJECT_ROOT / "ml" / "artifacts"
DEFAULT_MODEL_PATH = ARTIFACTS_DIR / "phishing_model.keras"
DEFAULT_SCALER_PATH = ARTIFACTS_DIR / "scaler.pkl"

PHISHING_THRESHOLD = 0.5
MEDIUM_RISK_THRESHOLD = 0.4
HIGH_RISK_THRESHOLD = 0.75


class PhishingPredictor:
    """Loads model artifacts and predicts phishing risk for URLs."""

    def __init__(
        self,
        model_path: str | Path = DEFAULT_MODEL_PATH,
        scaler_path: str | Path = DEFAULT_SCALER_PATH,
    ) -> None:
        self.model_path = Path(model_path)
        self.scaler_path = Path(scaler_path)
        self.model = self._load_model(self.model_path)
        self.scaler = self._load_scaler(self.scaler_path)

    def predict(self, url: str) -> dict[str, str | float]:
        """Predict whether a URL is phishing or legitimate.

        Args:
            url: Raw URL supplied by the API, dashboard, or Chrome extension.

        Returns:
            Dictionary containing prediction label, confidence percentage, and
            risk level.
        """

        normalized_url = self._normalize_url(url)
        self._validate_url(normalized_url)

        feature_vector = np.array([extract_features(normalized_url)], dtype=float)
        scaled_features = self.scaler.transform(feature_vector)

        phishing_probability = float(self.model.predict(scaled_features, verbose=0).ravel()[0])
        prediction = "Phishing" if phishing_probability >= PHISHING_THRESHOLD else "Legitimate"
        confidence = self._confidence_percentage(phishing_probability, prediction)
        risk_level = self._risk_level(phishing_probability)

        return {
            "prediction": prediction,
            "confidence": confidence,
            "risk_level": risk_level,
        }

    def predict_url(self, url: str) -> dict[str, str | float]:
        """Backward-compatible alias for callers that use predict_url."""

        return self.predict(url)

    def _load_model(self, model_path: Path) -> tf.keras.Model:
        """Load the trained TensorFlow/Keras model from disk."""

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model artifact not found: {model_path}. Train the model before running inference."
            )
        return tf.keras.models.load_model(model_path)

    def _load_scaler(self, scaler_path: Path) -> Any:
        """Load the fitted StandardScaler used during model training."""

        if not scaler_path.exists():
            raise FileNotFoundError(
                f"Scaler artifact not found: {scaler_path}. Train the model before running inference."
            )
        return joblib.load(scaler_path)

    def _normalize_url(self, url: str) -> str:
        """Normalize common user input before parsing and feature extraction."""

        cleaned_url = str(url).strip()
        if not cleaned_url:
            raise ValueError("URL cannot be empty.")
        if cleaned_url.startswith(("http://", "https://")):
            return cleaned_url
        return f"http://{cleaned_url}"

    def _validate_url(self, url: str) -> None:
        """Validate that the normalized URL has the minimum required structure."""

        parsed_url = urlparse(url)
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ValueError(f"Invalid URL supplied for prediction: {url}")

    def _confidence_percentage(self, phishing_probability: float, prediction: str) -> float:
        """Return confidence for the selected class as a percentage."""

        confidence = phishing_probability if prediction == "Phishing" else 1.0 - phishing_probability
        return round(confidence * 100, 2)

    def _risk_level(self, phishing_probability: float) -> str:
        """Map phishing probability to Low, Medium, or High risk."""

        if phishing_probability >= HIGH_RISK_THRESHOLD:
            return "High"
        if phishing_probability >= MEDIUM_RISK_THRESHOLD:
            return "Medium"
        return "Low"


def predict_url(url: str) -> dict[str, str | float]:
    """Convenience function for one-off URL predictions."""

    predictor = PhishingPredictor()
    return predictor.predict(url)


def main() -> None:
    """Small command-line helper for manual inference checks."""

    import argparse

    parser = argparse.ArgumentParser(description="Predict phishing risk for a URL.")
    parser.add_argument("url", help="URL to analyze")
    args = parser.parse_args()

    result = predict_url(args.url)
    print(result)


if __name__ == "__main__":
    main()
