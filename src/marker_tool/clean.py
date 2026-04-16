import re


def normalize_marker(marker: str):
    """
    Normalize marker name (spacing, separators).
    No synonym mapping.
    """

    if not marker:
        return ""

    # strip whitespace
    marker = marker.strip()

    # normalize separators
    marker = re.sub(r"[-_]", " ", marker)

    # collapse multiple spaces
    marker = re.sub(r"\s+", " ", marker)

    return marker