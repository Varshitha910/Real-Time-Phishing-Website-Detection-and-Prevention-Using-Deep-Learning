"""Unified feature extraction pipeline for training and inference."""

from ml.feature_extraction.content_features import extract_content_features
from ml.feature_extraction.domain_features import extract_domain_features
from ml.feature_extraction.lexical_features import extract_lexical_features
from ml.feature_extraction.network_features import extract_network_features


def extract_features(url: str, html: str | None = None) -> dict[str, int | float | bool]:
    """Combine all feature groups into one model-ready dictionary."""

    return {
        **extract_lexical_features(url),
        **extract_domain_features(url),
        **extract_network_features(url),
        **extract_content_features(html),
    }

