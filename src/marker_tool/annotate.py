from marker_tool.search import find_best_ensg
from marker_tool.hpa import (
    fetch_hpa_json,
    extract_location_strings,
    categorize_localization,
    infer_segmentation,
    extract_gene_description,
)
from marker_tool.utils import safe_str


def empty_result(marker: str, comment: str = ""):
    """
    Return empty annotation result.
    """
    return {
        "marker": marker,
        "gene_symbol": "",
        "subcellular_localization": "",
        "whole_cell_segmentation": "",
        "hpa_entry": "",
        "gene_description": "",
        "comments": comment,
    }


def annotate_marker(marker: str, allow_direct_gene: bool = False):
    """
    Annotate one marker using Human Protein Atlas.
    """
    marker = safe_str(marker)

    if not marker:
        return empty_result(marker)

    ensg = find_best_ensg(marker)

    if not ensg and allow_direct_gene:
        ensg = find_best_ensg(marker)

    if not ensg:
        return empty_result(marker, "Marker not found in Human Protein Atlas search")

    data = fetch_hpa_json(ensg) or {}

    gene_symbol = safe_str(data.get("Gene", ""))
    locations = extract_location_strings(data)
    localization = categorize_localization(locations)
    segmentation = infer_segmentation(localization)
    description = extract_gene_description(data)

    return {
        "marker": marker,
        "gene_symbol": gene_symbol,
        "subcellular_localization": localization,
        "whole_cell_segmentation": segmentation,
        "hpa_entry": ensg,
        "gene_description": description,
        "comments": "",
    }