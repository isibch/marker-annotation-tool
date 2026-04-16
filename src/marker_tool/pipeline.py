import pandas as pd
from pathlib import Path

from marker_tool.inputs import load_input
from marker_tool.extract import extract_marker
from marker_tool.clean import normalize_marker
from marker_tool.annotate import annotate_marker


def run_pipeline(input_path, output_path, allow_direct_gene=False, recursive=False):
    """
    Run the full marker processing pipeline and save results as CSV.
    """
    records = load_input(input_path, recursive=recursive)
    results = []

    input_path_obj = Path(input_path)

    if input_path_obj.is_dir():
        print(f"Found {len(records)} files in folder: {input_path_obj.name}")
    else:
        print(f"Found {len(records)} records in input: {input_path_obj.name}")

    total = len(records)

    for i, record in enumerate(records, start=1):
        raw_input = record
        source_filename = ""

        if Path(record).suffix:
            source_filename = Path(record).stem

        print(f"[{i}/{total}] Processing: {record}")

        marker = extract_marker(record)
        marker = normalize_marker(marker)
        annotation = annotate_marker(marker, allow_direct_gene=allow_direct_gene)

        annotation["raw_input"] = raw_input
        annotation["source_filename"] = source_filename

        results.append(annotation)

    df = pd.DataFrame(results)
    df.to_csv(output_path, index=False)

    print(f"Saved results to: {output_path}")
    print("Completed successfully")