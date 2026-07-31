"""Train the deep learning phishing URL classifier.

This script loads the cleaned URL dataset, extracts numerical URL features,
splits the data into train/validation/test sets, scales the features, trains a
TensorFlow/Keras neural network, evaluates the final model, and saves all
training artifacts needed by the inference API.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from ml.feature_extraction.url_features import FEATURE_COLUMNS, extract_dataframe_features


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "data" / "processed" / "cleaned_dataset.csv"
ARTIFACTS_DIR = PROJECT_ROOT / "ml" / "artifacts"

MODEL_PATH = ARTIFACTS_DIR / "phishing_model.keras"
SCALER_PATH = ARTIFACTS_DIR / "scaler.pkl"
METRICS_PATH = ARTIFACTS_DIR / "model_metrics.json"
TRAINING_PLOT_PATH = ARTIFACTS_DIR / "training_history.png"

URL_COLUMN = "url"
LABEL_COLUMN = "label"
RANDOM_SEED = 42
TEST_SIZE = 0.15
VALIDATION_SIZE = 0.15
EPOCHS = 50
BATCH_SIZE = 64


def load_cleaned_dataset(dataset_path: str | Path = DATASET_PATH) -> pd.DataFrame:
    """Load the cleaned URL dataset created by preprocessing."""

    path = Path(dataset_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found: {path}. Run ml/preprocessing/dataset_loader.py first."
        )

    dataset = pd.read_csv(path)
    required_columns = {URL_COLUMN, LABEL_COLUMN}
    missing_columns = required_columns.difference(dataset.columns)
    if missing_columns:
        raise ValueError(f"Cleaned dataset is missing columns: {sorted(missing_columns)}")
    if dataset.empty:
        raise ValueError("Cleaned dataset is empty.")

    dataset = dataset.dropna(subset=[URL_COLUMN, LABEL_COLUMN]).copy()
    dataset[LABEL_COLUMN] = dataset[LABEL_COLUMN].astype(int)
    if not set(dataset[LABEL_COLUMN].unique()).issubset({0, 1}):
        raise ValueError("Label column must contain only binary values: 0 and 1.")

    return dataset.reset_index(drop=True)


def build_model(input_dim: int) -> tf.keras.Model:
    """Build the required TensorFlow/Keras binary classification model."""

    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(input_dim,), name="url_feature_input"),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ],
        name="phishing_url_classifier",
    )

    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )
    return model


def split_dataset(
    features: pd.DataFrame,
    labels: pd.Series,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series]:
    """Split features and labels into train, validation, and test sets.

    Final split:
    - Train: 70%
    - Validation: 15%
    - Test: 15%
    """

    x_train_validation, x_test, y_train_validation, y_test = train_test_split(
        features,
        labels,
        test_size=TEST_SIZE,
        random_state=RANDOM_SEED,
        stratify=labels,
    )

    validation_ratio = VALIDATION_SIZE / (1.0 - TEST_SIZE)
    x_train, x_validation, y_train, y_validation = train_test_split(
        x_train_validation,
        y_train_validation,
        test_size=validation_ratio,
        random_state=RANDOM_SEED,
        stratify=y_train_validation,
    )

    return x_train, x_validation, x_test, y_train, y_validation, y_test


def scale_features(
    x_train: pd.DataFrame,
    x_validation: pd.DataFrame,
    x_test: pd.DataFrame,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, StandardScaler]:
    """Fit StandardScaler on training data and transform all feature splits."""

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_validation_scaled = scaler.transform(x_validation)
    x_test_scaled = scaler.transform(x_test)
    return x_train_scaled, x_validation_scaled, x_test_scaled, scaler


def create_callbacks() -> list[tf.keras.callbacks.Callback]:
    """Create EarlyStopping and ModelCheckpoint callbacks."""

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    return [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=6,
            restore_best_weights=True,
            verbose=1,
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=MODEL_PATH,
            monitor="val_loss",
            save_best_only=True,
            verbose=1,
        ),
    ]


def evaluate_model(model: tf.keras.Model, x_test: np.ndarray, y_test: pd.Series) -> dict[str, Any]:
    """Evaluate the trained model using security-relevant classification metrics."""

    y_scores = model.predict(x_test, verbose=0).ravel()
    y_predictions = (y_scores >= 0.5).astype(int)

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_predictions)),
        "precision": float(precision_score(y_test, y_predictions, zero_division=0)),
        "recall": float(recall_score(y_test, y_predictions, zero_division=0)),
        "f1_score": float(f1_score(y_test, y_predictions, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, y_scores)),
        "confusion_matrix": confusion_matrix(y_test, y_predictions).tolist(),
        "threshold": 0.5,
        "feature_columns": FEATURE_COLUMNS,
    }
    return metrics


def save_metrics(metrics: dict[str, Any], metrics_path: str | Path = METRICS_PATH) -> None:
    """Save model metrics as JSON for dashboard and documentation use."""

    path = Path(metrics_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as metrics_file:
        json.dump(metrics, metrics_file, indent=2)


def plot_training_history(history: tf.keras.callbacks.History) -> None:
    """Save training and validation accuracy/loss curves."""

    history_values = history.history
    epochs = range(1, len(history_values.get("loss", [])) + 1)

    plt.figure(figsize=(12, 5))

    # Accuracy chart helps detect underfitting or overfitting during training.
    plt.subplot(1, 2, 1)
    plt.plot(epochs, history_values.get("accuracy", []), label="Training Accuracy")
    plt.plot(epochs, history_values.get("val_accuracy", []), label="Validation Accuracy")
    plt.title("Training vs Validation Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Loss chart shows whether validation performance degrades after training.
    plt.subplot(1, 2, 2)
    plt.plot(epochs, history_values.get("loss", []), label="Training Loss")
    plt.plot(epochs, history_values.get("val_loss", []), label="Validation Loss")
    plt.title("Training vs Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Binary Crossentropy Loss")
    plt.legend()
    plt.grid(True, alpha=0.3)

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(TRAINING_PLOT_PATH, dpi=160)
    plt.close()


def train_model() -> dict[str, Any]:
    """Run the complete model training and artifact generation workflow."""

    tf.keras.utils.set_random_seed(RANDOM_SEED)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

    dataset = load_cleaned_dataset()

    # Convert raw URLs into numeric vectors in a stable feature order.
    features = extract_dataframe_features(dataset[[URL_COLUMN]])
    labels = dataset[LABEL_COLUMN]

    x_train, x_validation, x_test, y_train, y_validation, y_test = split_dataset(features, labels)
    x_train_scaled, x_validation_scaled, x_test_scaled, scaler = scale_features(x_train, x_validation, x_test)

    model = build_model(input_dim=len(FEATURE_COLUMNS))
    history = model.fit(
        x_train_scaled,
        y_train,
        validation_data=(x_validation_scaled, y_validation),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=create_callbacks(),
        verbose=1,
    )

    # Ensure the final saved file contains the best weights restored by EarlyStopping.
    model.save(MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)

    metrics = evaluate_model(model, x_test_scaled, y_test)
    save_metrics(metrics)
    plot_training_history(history)

    return metrics


def main() -> None:
    """Command-line entry point for model training."""

    metrics = train_model()
    print(f"Model saved to: {MODEL_PATH}")
    print(f"Scaler saved to: {SCALER_PATH}")
    print(f"Metrics saved to: {METRICS_PATH}")
    print(f"Training plot saved to: {TRAINING_PLOT_PATH}")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
