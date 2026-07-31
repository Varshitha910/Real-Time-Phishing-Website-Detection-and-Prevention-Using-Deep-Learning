"""SHAP explainability for individual phishing URL predictions.

This module loads the trained Keras phishing model and fitted StandardScaler,
extracts the same URL features used during training, generates SHAP values, and
returns the top contributing features for a single prediction.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import joblib
import numpy as np
import shap
import tensorflow as tf

from ml.feature_extraction.url_features import FEATURE_COLUMNS, extract_features


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS_DIR = PROJECT_ROOT / "ml" / "artifacts"
DEFAULT_MODEL_PATH = ARTIFACTS_DIR / "phishing_model.keras"
DEFAULT_SCALER_PATH = ARTIFACTS_DIR / "scaler.pkl"

PHISHING_THRESHOLD = 0.5
DEFAULT_TOP_FEATURES = 5


class ShapExplainer:
    """Generate SHAP explanations for the trained phishing classifier."""

    def __init__(
        self,
        model_path: str | Path = DEFAULT_MODEL_PATH,
        scaler_path: str | Path = DEFAULT_SCALER_PATH,
        background_samples: np.ndarray | None = None,
    ) -> None:
        self.model_path = Path(model_path)
        self.scaler_path = Path(scaler_path)
        self.model = self._load_model(self.model_path)
        self.scaler = self._load_scaler(self.scaler_path)
        self.background_samples = background_samples if background_samples is not None else self._default_background()
        self.explainer = self._build_explainer()

    def explain_url(self, url: str, top_n: int = DEFAULT_TOP_FEATURES) -> dict[str, Any]:
        """Explain an individual URL prediction.

        Args:
            url: Raw URL to classify and explain.
            top_n: Number of strongest feature impacts to return.

        Returns:
            Dictionary containing the prediction label and top SHAP features.
        """

        normalized_url = self._normalize_url(url)
        self._validate_url(normalized_url)

        raw_features = np.array([extract_features(normalized_url)], dtype=float)
        scaled_features = self.scaler.transform(raw_features)

        phishing_probability = float(self.model.predict(scaled_features, verbose=0).ravel()[0])
        prediction = "Phishing" if phishing_probability >= PHISHING_THRESHOLD else "Legitimate"
        shap_values = self._calculate_shap_values(scaled_features)
        top_features = self._top_contributing_features(shap_values, top_n)

        return {
            "prediction": prediction,
            "top_features": top_features,
        }

    def explain(self, url: str, top_n: int = DEFAULT_TOP_FEATURES) -> dict[str, Any]:
        """Backward-compatible alias for explain_url."""

        return self.explain_url(url, top_n=top_n)

    def _load_model(self, model_path: Path) -> tf.keras.Model:
        """Load the trained Keras model artifact."""

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model artifact not found: {model_path}. Train the model before generating SHAP explanations."
            )
        return tf.keras.models.load_model(model_path)

    def _load_scaler(self, scaler_path: Path) -> Any:
        """Load the fitted StandardScaler used during training."""

        if not scaler_path.exists():
            raise FileNotFoundError(
                f"Scaler artifact not found: {scaler_path}. Train the model before generating SHAP explanations."
            )
        return joblib.load(scaler_path)

    def _default_background(self) -> np.ndarray:
        """Create a stable SHAP background sample in scaled feature space.

        StandardScaler transforms feature means to zero, so a zero vector is a
        practical baseline when the original training background sample is not
        saved as an artifact.
        """

        return np.zeros((1, len(FEATURE_COLUMNS)), dtype=float)

    def _build_explainer(self) -> shap.KernelExplainer:
        """Build a model-agnostic SHAP explainer for the Keras classifier."""

        return shap.KernelExplainer(self._predict_probability, self.background_samples)

    def _predict_probability(self, scaled_features: np.ndarray) -> np.ndarray:
        """Return phishing probabilities for SHAP's perturbation samples."""

        predictions = self.model.predict(np.asarray(scaled_features, dtype=float), verbose=0)
        return predictions.reshape(-1)

    def _calculate_shap_values(self, scaled_features: np.ndarray) -> np.ndarray:
        """Generate SHAP values for one scaled URL feature vector."""

        shap_values = self.explainer.shap_values(scaled_features, nsamples="auto")
        return self._coerce_single_output_shap_values(shap_values)

    def _coerce_single_output_shap_values(self, shap_values: Any) -> np.ndarray:
        """Normalize SHAP output shapes across SHAP versions."""

        if isinstance(shap_values, list):
            shap_values = shap_values[0]

        values = np.asarray(shap_values, dtype=float)
        if values.ndim == 3:
            values = values[:, :, 0]
        if values.ndim == 2:
            values = values[0]
        return values.reshape(-1)

    def _top_contributing_features(self, shap_values: np.ndarray, top_n: int) -> list[dict[str, float | str]]:
        """Return the strongest feature impacts sorted by absolute SHAP value."""

        ranked_indexes = np.argsort(np.abs(shap_values))[::-1][:top_n]
        return [
            {
                "feature": FEATURE_COLUMNS[index],
                "impact": round(float(shap_values[index]), 6),
            }
            for index in ranked_indexes
        ]

    def _normalize_url(self, url: str) -> str:
        """Normalize user-supplied URLs before validation and feature extraction."""

        cleaned_url = str(url).strip()
        if not cleaned_url:
            raise ValueError("URL cannot be empty.")
        if cleaned_url.startswith(("http://", "https://")):
            return cleaned_url
        return f"http://{cleaned_url}"

    def _validate_url(self, url: str) -> None:
        """Validate that a URL has an HTTP scheme and network location."""

        parsed_url = urlparse(url)
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ValueError(f"Invalid URL supplied for explanation: {url}")


def explain_url(url: str, top_n: int = DEFAULT_TOP_FEATURES) -> dict[str, Any]:
    """Convenience function for one-off SHAP explanations."""

    explainer = ShapExplainer()
    return explainer.explain_url(url, top_n=top_n)


def main() -> None:
    """Command-line helper for manually explaining a URL prediction."""

    import argparse
    import json

    parser = argparse.ArgumentParser(description="Explain a phishing model prediction for a URL.")
    parser.add_argument("url", help="URL to classify and explain")
    parser.add_argument("--top-n", type=int, default=DEFAULT_TOP_FEATURES, help="Number of top features to show")
    args = parser.parse_args()

    result = explain_url(args.url, top_n=args.top_n)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
