"""Train the backend phishing model and save model.h5 plus scaler.pkl."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from backend.ml.feature_extraction import FEATURE_COLUMNS, feature_vector


ML_DIR = Path(__file__).resolve().parent
DATASET_PATH = ML_DIR / "dataset.csv"
MODEL_PATH = ML_DIR / "model.h5"
SCALER_PATH = ML_DIR / "scaler.pkl"
METRICS_PATH = ML_DIR / "metrics.json"


def train() -> dict[str, object]:
    """Train a dense neural network on URL features."""

    dataset = pd.read_csv(DATASET_PATH)
    if not {"url", "label"}.issubset(dataset.columns):
        raise ValueError("dataset.csv must contain url and label columns.")

    x = np.array([feature_vector(url) for url in dataset["url"]], dtype=float)
    y = dataset["label"].astype(int).to_numpy()

    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(len(FEATURE_COLUMNS),)),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ]
    )
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    model.fit(x_train_scaled, y_train, validation_split=0.15, epochs=40, batch_size=16, verbose=1)

    probabilities = model.predict(x_test_scaled, verbose=0).ravel()
    predictions = (probabilities >= 0.5).astype(int)
    metrics = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "classification_report": classification_report(y_test, predictions, output_dict=True, zero_division=0),
        "feature_columns": FEATURE_COLUMNS,
    }

    model.save(MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


if __name__ == "__main__":
    print(json.dumps(train(), indent=2))

