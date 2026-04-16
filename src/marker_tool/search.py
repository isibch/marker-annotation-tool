import re
import requests

from marker_tool.constants import SEARCH_URL
from marker_tool.http import fetch
from marker_tool.utils import normalize_text
from marker_tool.hpa import fetch_hpa_json


def normalize_for_match(text: str) -> str:
    """
    Normalize text for marker comparison.
    """
    return re.sub(r"[\s\-_./]+", "", text.strip().lower())


def find_best_ensg(marker: str):
    """
    Search HPA and return best matching ENSG id.
    """

    query = marker.strip()
    if not query:
        return None

    marker_norm = normalize_for_match(query)
    url = SEARCH_URL.format(requests.utils.quote(query))

    try:
        response = fetch(url)
    except Exception:
        return None

    html = response.text

    # extract ENSG ids from links
    link_pattern = re.compile(r'href="[^"]*/(ENSG\d+)(?:-([^"?#/]*))?[^"]*"')

    seen = set()
    candidates = []

    for match in link_pattern.finditer(html):
        ensg = match.group(1)
        slug = normalize_for_match(match.group(2) or "")

        if ensg not in seen:
            seen.add(ensg)
            candidates.append((ensg, slug))

    if not candidates:
        return None

    # exact gene symbol match
    for ensg, slug in candidates:
        if marker_norm == slug:
            return ensg

    # check gene synonyms in JSON
    for ensg, _ in candidates[:10]:
        data = fetch_hpa_json(ensg)
        if data is None:
            continue

        synonyms = data.get("Gene synonym", [])

        if isinstance(synonyms, str):
            synonyms = [s.strip() for s in synonyms.split(",")]

        gene_symbol = data.get("Gene", "")

        all_names = {normalize_for_match(s) for s in synonyms if s}
        all_names.add(normalize_for_match(gene_symbol))

        if marker_norm in all_names:
            return ensg

    # fallback → first search result
    return candidates[0][0]