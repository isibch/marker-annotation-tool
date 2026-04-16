# central place for configuration and constant values

BASE_URL = "https://www.proteinatlas.org"
SEARCH_URL = BASE_URL + "/search/{}"
JSON_URL = BASE_URL + "/{ensg}.json"

REQUEST_TIMEOUT = 30
DEFAULT_SLEEP_SECS = 1.0
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

USER_AGENT = "Mozilla/5.0 (compatible; marker-annotation-script/1.0)"

# patterns removed from marker names before HPA search
NOISE_PATTERNS = [
    r"^CB-T\d+\.\d+\s+TMA\s+",
    r"^TMA\s+",
]

# fixed output structure for annotation tables
OUTPUT_COLUMNS = [
    "marker",
    "gene_symbol",
    "subcellular_localization",
    "whole_cell_segmentation",
    "hpa_entry",
    "gene_description",
    "comments",
]

# keys used in HPA JSON to locate subcellular localization data
LOCATION_PARENT_KEYS = [
    "Subcellular location",
    "subcellular_location",
    "subcellular",
]

LOCATION_EVIDENCE_KEYS = [
    "Enhanced", "Supported", "Approved", "Uncertain",
    "enhanced", "supported", "approved", "uncertain",
    "main_location", "additional_location",
    "main location", "additional location",
]

# localization term groups
MEMBRANE_TERMS = frozenset([
    "plasma membrane", "cell membrane", "membrane",
    "cell junction", "lateral membrane",
])

NUCLEAR_TERMS = frozenset([
    "nucleus", "nucleoplasm", "nuclear", "nucleoli",
    "nuclear speckles", "nuclear membrane", "nuclear bodies",
    "nuclear lamina",
])

CYTOPLASMIC_TERMS = frozenset([
    "cytoplasm", "cytosol", "golgi apparatus", "golgi",
    "endoplasmic reticulum", "vesicles", "mitochondria",
    "intermediate filaments", "microtubules", "actin filaments",
    "intracellular", "lysosome", "endosome", "peroxisome",
    "centrosome", "centriolar satellite",
])