"""Dataset cleaning utilities.

These functions remove invalid rows, normalize URL text, and prepare the data
for feature extraction.
"""

import pandas as pd


def clean_url_dataset(dataset: pd.DataFrame, url_column: str = "url") -> pd.DataFrame:
    """Drop empty, duplicate, and malformed URL rows from a dataset."""

    cleaned = dataset.copy()
    cleaned[url_column] = cleaned[url_column].astype(str).str.strip()
    cleaned = cleaned[cleaned[url_column].str.len() > 0]
    cleaned = cleaned.drop_duplicates(subset=[url_column])
    return cleaned.reset_index(drop=True)

