"""Model and training configuration values."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelConfig:
    """Default neural network training configuration."""

    input_dim: int
    hidden_units: tuple[int, ...] = (128, 64, 32)
    dropout_rate: float = 0.25
    learning_rate: float = 0.001
    batch_size: int = 64
    epochs: int = 30

