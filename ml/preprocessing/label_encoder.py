"""Label encoding helpers.

The model expects numeric labels, while datasets often use strings such as
phishing, legitimate, malicious, or benign.
"""

import pandas as pd


LABEL_MAPPING = {
    "legitimate": 0,
    "benign": 0,
    "safe": 0,
    "phishing": 1,
    "malicious": 1,
}


def encode_labels(dataset: pd.DataFrame, label_column: str = "label") -> pd.DataFrame:
    """Convert text labels into binary numeric labels."""

    encoded = dataset.copy()
    encoded[label_column] = encoded[label_column].astype(str).str.lower().map(LABEL_MAPPING)
    if encoded[label_column].isna().any():
        raise ValueError("Dataset contains labels that are not in LABEL_MAPPING.")
    return encoded

