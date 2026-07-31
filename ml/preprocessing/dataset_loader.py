"""Load, label, merge, clean, shuffle, and save URL datasets.

This module prepares the first production-ready dataset used by the phishing
detection model. It expects two raw CSV files:

- data/raw/phishing_urls.csv
- data/raw/legitimate_urls.csv

The output is a clean binary classification dataset saved to:

- data/processed/cleaned_dataset.csv
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

PHISHING_DATASET_PATH = RAW_DATA_DIR / "phishing_urls.csv"
LEGITIMATE_DATASET_PATH = RAW_DATA_DIR / "legitimate_urls.csv"
CLEANED_DATASET_PATH = PROCESSED_DATA_DIR / "cleaned_dataset.csv"

URL_COLUMN = "url"
LABEL_COLUMN = "label"
PHISHING_LABEL = 1
LEGITIMATE_LABEL = 0
RANDOM_SEED = 42

# Common URL column names found in public phishing datasets.
URL_COLUMN_CANDIDATES = (
    "url",
    "URL",
    "Url",
    "link",
    "Link",
    "website",
    "Website",
    "domain",
    "Domain",
)


def load_csv_dataset(path: str | Path) -> pd.DataFrame:
    """Load a CSV file into a DataFrame with clear validation errors."""

    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")
    if dataset_path.suffix.lower() != ".csv":
        raise ValueError(f"Only CSV datasets are supported: {dataset_path}")

    dataset = pd.read_csv(dataset_path)
    if dataset.empty:
        raise ValueError(f"Dataset is empty: {dataset_path}")

    return dataset


def prepare_labeled_dataset(dataset: pd.DataFrame, label: int) -> pd.DataFrame:
    """Return a normalized two-column dataset containing url and label."""

    url_column = find_url_column(dataset)

    # Keep only the URL needed for supervised training and attach the class.
    labeled = dataset[[url_column]].copy()
    labeled.columns = [URL_COLUMN]
    labeled[LABEL_COLUMN] = label
    return labeled


def find_url_column(dataset: pd.DataFrame) -> str:
    """Find the column containing URL values.

    Public datasets use inconsistent column names. This helper keeps the
    pipeline practical while still failing loudly if no URL-like column exists.
    """

    for candidate in URL_COLUMN_CANDIDATES:
        if candidate in dataset.columns:
            return candidate

    available_columns = ", ".join(str(column) for column in dataset.columns)
    raise ValueError(f"No URL column found. Available columns: {available_columns}")


def merge_url_datasets(phishing: pd.DataFrame, legitimate: pd.DataFrame) -> pd.DataFrame:
    """Combine phishing and legitimate URL records into one dataset."""

    phishing_labeled = prepare_labeled_dataset(phishing, PHISHING_LABEL)
    legitimate_labeled = prepare_labeled_dataset(legitimate, LEGITIMATE_LABEL)
    return pd.concat([phishing_labeled, legitimate_labeled], ignore_index=True)


def clean_dataset(dataset: pd.DataFrame) -> pd.DataFrame:
    """Remove null, blank, duplicate, and invalid records."""

    cleaned = dataset.copy()

    # Normalize impossible values to NaN so pandas can remove them reliably.
    cleaned.replace([np.inf, -np.inf], np.nan, inplace=True)
    cleaned.dropna(subset=[URL_COLUMN, LABEL_COLUMN], inplace=True)

    cleaned[URL_COLUMN] = cleaned[URL_COLUMN].astype(str).str.strip()
    cleaned = cleaned[cleaned[URL_COLUMN].str.len() > 0]
    cleaned = cleaned[cleaned[LABEL_COLUMN].isin([LEGITIMATE_LABEL, PHISHING_LABEL])]

    # Deduplicate by URL after normalization so repeated samples do not bias the model.
    cleaned.drop_duplicates(subset=[URL_COLUMN], keep="first", inplace=True)
    cleaned[LABEL_COLUMN] = cleaned[LABEL_COLUMN].astype(int)

    return cleaned[[URL_COLUMN, LABEL_COLUMN]].reset_index(drop=True)


def shuffle_dataset(dataset: pd.DataFrame, random_seed: int = RANDOM_SEED) -> pd.DataFrame:
    """Shuffle rows to avoid class ordering effects during downstream training."""

    return dataset.sample(frac=1.0, random_state=random_seed).reset_index(drop=True)


def save_cleaned_dataset(dataset: pd.DataFrame, output_path: str | Path = CLEANED_DATASET_PATH) -> Path:
    """Save the cleaned dataset and return the written file path."""

    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    dataset.to_csv(destination, index=False)
    return destination


def build_cleaned_dataset(
    phishing_path: str | Path = PHISHING_DATASET_PATH,
    legitimate_path: str | Path = LEGITIMATE_DATASET_PATH,
    output_path: str | Path = CLEANED_DATASET_PATH,
) -> pd.DataFrame:
    """Run the complete dataset loading and cleaning workflow."""

    phishing_dataset = load_csv_dataset(phishing_path)
    legitimate_dataset = load_csv_dataset(legitimate_path)

    merged_dataset = merge_url_datasets(phishing_dataset, legitimate_dataset)
    cleaned_dataset = clean_dataset(merged_dataset)
    shuffled_dataset = shuffle_dataset(cleaned_dataset)
    save_cleaned_dataset(shuffled_dataset, output_path)

    return shuffled_dataset


def main() -> None:
    """Create data/processed/cleaned_dataset.csv from the raw URL datasets."""

    cleaned_dataset = build_cleaned_dataset()
    print(f"Cleaned dataset saved to: {CLEANED_DATASET_PATH}")
    print(f"Total records: {len(cleaned_dataset)}")
    print(cleaned_dataset[LABEL_COLUMN].value_counts().sort_index().to_string())


if __name__ == "__main__":
    main()
