"""Train, validation, and test splitting utilities."""

from dataclasses import dataclass

import pandas as pd
from sklearn.model_selection import train_test_split


@dataclass(frozen=True)
class DatasetSplit:
    """Container for split datasets."""

    train: pd.DataFrame
    validation: pd.DataFrame
    test: pd.DataFrame


def split_dataset(
    dataset: pd.DataFrame,
    label_column: str = "label",
    test_size: float = 0.15,
    validation_size: float = 0.15,
    random_state: int = 42,
) -> DatasetSplit:
    """Split data into train, validation, and test sets using stratified labels."""

    train_validation, test = train_test_split(
        dataset,
        test_size=test_size,
        random_state=random_state,
        stratify=dataset[label_column],
    )
    validation_ratio = validation_size / (1.0 - test_size)
    train, validation = train_test_split(
        train_validation,
        test_size=validation_ratio,
        random_state=random_state,
        stratify=train_validation[label_column],
    )
    return DatasetSplit(train=train, validation=validation, test=test)

