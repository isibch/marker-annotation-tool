# Marker Tool

Tool for extracting and annotating biological markers using the Human Protein Atlas (HPA).

The tool can:
- extract markers from filenames
- process marker lists from `.txt` or `.csv`
- annotate markers using the Human Protein Atlas
- infer **subcellular localization** and **segmentation suitability**
- export results as a structured CSV table

---

# Installation

Clone the repository and install the package locally.

pip install -e .

Dependencies:
- pandas
- requests

---

# Usage

## Annotate a single marker

marker-tool query BCL2

Example output:

marker: BCL2
gene_symbol: BCL2
subcellular_localization: nuclear
whole_cell_segmentation: no
hpa_entry: ENSG00000171791
gene_description: BCL2 apoptosis regulator
comments:

---

## Annotate a list of markers

Create a text file:

markers.txt

Example:

BCL2
CD20
CA9
HER2

Run:

marker-tool run markers.txt -o results.csv

---

## Annotate markers from filenames in a folder

Example filenames:

BCL2 (23) CB-T1.0 TMA AcpH9 07.07.2025 am Omnis.svs
CA 9 (307) CB-T1.0 TMA AcpH9 07.07.2025 am Omnis.svs

Run:

marker-tool run slides_folder/ -o results.csv

Recursive search:

marker-tool run slides_folder/ --recursive -o results.csv

---

# Output

The resulting CSV contains the following columns:

marker
gene_symbol
subcellular_localization
whole_cell_segmentation
hpa_entry
gene_description
comments
raw_input
source_filename

Example:

marker,gene_symbol,subcellular_localization,whole_cell_segmentation,hpa_entry,gene_description,source_filename
CA9,CA9,membranous,yes,ENSG00000143970,Carbonic anhydrase 9,CA 9 (307) CB-T1.0 TMA

---

# Data Source

Human Protein Atlas  
https://www.proteinatlas.org

Gene information is retrieved via the HPA JSON API.

---

# Project Structure

marker-tool/

src/marker_tool/
- cli.py
- pipeline.py
- inputs.py
- extract.py
- clean.py
- search.py
- hpa.py
- annotate.py
- utils.py
- constants.py

pyproject.toml

---

# Future Improvements

- marker synonym database
- caching of HPA queries
- progress bar for large batches
- test suite (pytest)