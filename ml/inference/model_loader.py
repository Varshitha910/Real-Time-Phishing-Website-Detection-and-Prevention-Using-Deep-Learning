"""Model and preprocessing artifact loading utilities."""

from pathlib import Path
from typing import Any

import joblib
import tensorflow as tf


def load_keras_model(path: str | Path) -> tf.keras.Model:
    """Load a saved Keras model artifact."""

    return tf.keras.models.load_model(Path(path))


def load_pickle_artifact(path: str | Path) -> Any:
    """Load a pickle/joblib artifact such as a scaler or encoder."""

    return joblib.load(Path(path))

