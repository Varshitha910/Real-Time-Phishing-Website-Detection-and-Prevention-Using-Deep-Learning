"""Hyperparameter tuning placeholder.

Use this file for controlled experiments over learning rate, dropout, layer
sizes, batch size, and classification thresholds.
"""

from ml.training.model_config import ModelConfig


def candidate_configs(input_dim: int) -> list[ModelConfig]:
    """Return a small starter search space for tuning experiments."""

    return [
        ModelConfig(input_dim=input_dim, hidden_units=(128, 64), dropout_rate=0.2),
        ModelConfig(input_dim=input_dim, hidden_units=(256, 128, 64), dropout_rate=0.3),
        ModelConfig(input_dim=input_dim, hidden_units=(64, 32), dropout_rate=0.15),
    ]

