from marker_tool.constants import (
    JSON_URL,
    LOCATION_PARENT_KEYS,
    LOCATION_EVIDENCE_KEYS,
    MEMBRANE_TERMS,
    NUCLEAR_TERMS,
    CYTOPLASMIC_TERMS,
)
from marker_tool.http import fetch
from marker_tool.utils import normalize_text


_json_cache = {}


def _iter_items(obj, path=""):
    """
    Recursively yield (path, value) pairs from nested JSON-like objects.
    """
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_path = f"{path}.{key}" if path else key
            yield from _iter_items(value, new_path)

    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            new_path = f"{path}[{i}]"
            yield from _iter_items(value, new_path)

    else:
        yield path, obj


def fetch_hpa_json(ensg: str):
    """
    Fetch HPA JSON for a gene.
    Uses in-memory caching to avoid repeated requests.
    """
    if ensg in _json_cache:
        return _json_cache[ensg]

    url = JSON_URL.format(ensg=ensg)

    try:
        data = fetch(url).json()
    except Exception:
        data = None

    _json_cache[ensg] = data
    return data


def extract_location_strings(data: dict):
    """
    Extract subcellular localization strings from HPA JSON.

    First try known keys, then fall back to a recursive scan.
    """
    found = []

    # pass 1: structured lookup
    for parent_key in LOCATION_PARENT_KEYS:
        parent = data.get(parent_key)

        if not isinstance(parent, dict):
            continue

        for child_key in LOCATION_EVIDENCE_KEYS:
            value = parent.get(child_key)

            if value is None:
                continue

            items = value if isinstance(value, list) else [value]

            for item in items:
                txt = normalize_text(item)
                if txt:
                    found.append(txt)

    # pass 2: recursive fallback
    if not found:
        for path, value in _iter_items(data):
            lower_path = path.lower()

            if "subcell" not in lower_path and "location" not in lower_path:
                continue

            txt = normalize_text(value)

            if txt and len(txt) < 300:
                found.append(txt)

    # remove duplicates while keeping order
    return list(dict.fromkeys(found))


def categorize_localization(location_strings):
    """
    Map raw localization strings to:
    membranous / nuclear / cytoplasmic
    """
    text = " | ".join(location_strings).lower()
    categories = []

    if any(term in text for term in MEMBRANE_TERMS):
        categories.append("membranous")

    if any(term in text for term in NUCLEAR_TERMS):
        categories.append("nuclear")

    if any(term in text for term in CYTOPLASMIC_TERMS):
        categories.append("cytoplasmic")

    return "/".join(dict.fromkeys(categories))


def infer_segmentation(localization: str):
    """
    Infer segmentation suitability from localization.
    """
    if not localization:
        return ""

    parts = set(localization.split("/"))

    if parts == {"nuclear"}:
        return "no"

    if "membranous" in parts:
        if parts == {"membranous"}:
            return "yes"
        return "partial"

    if "cytoplasmic" in parts:
        return "partial"

    return "no"


def extract_gene_description(data: dict):
    """
    Extract gene description from HPA JSON.
    """
    for key in (
        "Gene description",
        "gene_description",
        "Gene_description",
        "description",
    ):
        txt = normalize_text(data.get(key, ""))
        if txt:
            return txt

    # recursive fallback
    for path, value in _iter_items(data):
        if "gene_description" in path.lower():
            txt = normalize_text(value)
            if txt:
                return txt

    return ""