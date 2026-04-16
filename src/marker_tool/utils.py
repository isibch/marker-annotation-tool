import pandas as pd

def safe_str(value):
    """
    Convert None / NaN to empty string.
    Strip whitespace from normal strings.
    """
    if value is None:
        return ""

    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass

    return str(value).strip()


def normalize_text(value):
    """
    Convert lists to semicolon-separated strings.
    Keep normal strings unchanged.
    """
    if value is None:
        return ""

    if isinstance(value, (list, tuple)):
        return "; ".join(str(v).strip() for v in value if str(v).strip())

    return str(value).strip()