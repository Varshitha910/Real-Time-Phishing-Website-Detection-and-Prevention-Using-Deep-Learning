# # """Starter URL feature extraction.

# # The full project can expand this file with WHOIS, DNS, SSL, redirect, and
# # HTML content features. These lexical features are intentionally fast enough for
# # real-time API and Chrome Extension calls.
# # """

# # import math
# # import re
# # from collections import Counter
# # from urllib.parse import urlparse


# # SUSPICIOUS_KEYWORDS = {"login", "verify", "update", "secure", "account", "bank", "password", "confirm"}


# # def extract_url_features(url: str) -> dict[str, int | float | bool]:
# #     """Extract lightweight lexical and domain features from a URL."""

# #     parsed = urlparse(url)
# #     hostname = parsed.hostname or ""
# #     path_and_query = f"{parsed.path}?{parsed.query}" if parsed.query else parsed.path

# #     return {
# #         "url_length": len(url),
# #         "domain_length": len(hostname),
# #         "path_length": len(path_and_query),
# #         "dot_count": url.count("."),
# #         "hyphen_count": url.count("-"),
# #         "at_symbol_count": url.count("@"),
# #         "special_char_count": len(re.findall(r"[^A-Za-z0-9]", url)),
# #         "subdomain_count": max(len(hostname.split(".")) - 2, 0),
# #         "uses_https": parsed.scheme == "https",
# #         "has_ip_address": _has_ip_address(hostname),
# #         "suspicious_keyword_count": _count_suspicious_keywords(url),
# #         "url_entropy": round(_shannon_entropy(url), 4),
# #     }


# # def _has_ip_address(hostname: str) -> bool:
# #     """Detect IPv4 hostnames, a common phishing signal."""

# #     return bool(re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", hostname))


# # def _count_suspicious_keywords(url: str) -> int:
# #     """Count phishing-related keywords in a URL."""

# #     lowered = url.lower()
# #     return sum(1 for keyword in SUSPICIOUS_KEYWORDS if keyword in lowered)


# # def _shannon_entropy(value: str) -> float:
# #     """Measure randomness in the URL string."""

# #     if not value:
# #         return 0.0

# #     counts = Counter(value)
# #     length = len(value)
# #     return -sum((count / length) * math.log2(count / length) for count in counts.values())

# import math
# import re
# from collections import Counter
# from urllib.parse import urlparse


# SUSPICIOUS_KEYWORDS = {
#     "login",
#     "verify",
#     "update",
#     "secure",
#     "account",
#     "bank",
#     "password",
#     "confirm"
# }


# def extract_url_features(url: str):

#     parsed = urlparse(url)

#     hostname = parsed.hostname or ""

#     return {

#         "url_length": len(url),

#         "domain_length": len(hostname),

#         "dot_count": url.count("."),

#         "hyphen_count": url.count("-"),

#         "digit_count": sum(c.isdigit() for c in url),

#         "https_present": int(parsed.scheme == "https"),

#         "ip_address_present": int(_has_ip_address(hostname)),

#         "suspicious_keyword_count":
#             _count_suspicious_keywords(url),

#         "subdomain_count":
#             max(len(hostname.split(".")) - 2, 0),

#         "special_char_count":
#             len(re.findall(r"[^A-Za-z0-9]", url)),

#         "url_entropy":
#             round(_shannon_entropy(url),4)
#     }



# def get_feature_vector(features):

#     return [
#         features["url_length"],
#         features["domain_length"],
#         features["dot_count"],
#         features["hyphen_count"],
#         features["digit_count"],
#         features["https_present"],
#         features["ip_address_present"],
#         features["suspicious_keyword_count"],
#         features["subdomain_count"],
#         features["special_char_count"],
#         features["url_entropy"]
#     ]



# def _has_ip_address(hostname):

#     return bool(
#         re.fullmatch(
#             r"(?:\d{1,3}\.){3}\d{1,3}",
#             hostname
#         )
#     )



# def _count_suspicious_keywords(url):

#     url=url.lower()

#     return sum(
#         1 for k in SUSPICIOUS_KEYWORDS
#         if k in url
#     )



# def _shannon_entropy(value):

#     if not value:
#         return 0

#     counts = Counter(value)

#     length=len(value)

#     return -sum(
#         (count/length)*math.log2(count/length)
#         for count in counts.values()
#     )
from ml.feature_extraction.url_features import extract_features, FEATURE_COLUMNS


def extract_url_features(url):

    values = extract_features(url)

    return {
        FEATURE_COLUMNS[i]: values[i]
        for i in range(len(FEATURE_COLUMNS))
    }