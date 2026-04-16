import re
from pathlib import Path


def extract_marker(filename: str):
    """
    Extract marker name from a filename.
    """

    # remove file extension
    name = Path(filename).stem.strip()

    # remove known prefix like "CB-T1.0 TMA "
    name = re.sub(r"^CB-T\d+\.\d+\s*TMA\s+", "", name)

    # extract marker part before first "("
    match = re.search(r"^([^(]+)", name)

    if match:
        marker = match.group(1).strip()
    else:
        marker = name.strip()

    return marker