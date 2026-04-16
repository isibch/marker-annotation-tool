from pathlib import Path
import pandas as pd


def load_input(input_path, recursive=False):
    """
    Load input from folder, txt file, or csv file.
    Returns a list of strings.
    """
    input_path = Path(input_path)

    # folder input
    if input_path.is_dir():
        if recursive:
            files = [str(file) for file in input_path.rglob("*") if file.is_file()]
        else:
            files = [str(file) for file in input_path.iterdir() if file.is_file()]
        return files

    # file input
    if input_path.is_file():
        suffix = input_path.suffix.lower()

        # txt marker list
        if suffix == ".txt":
            with open(input_path, "r", encoding="utf-8") as f:
                return [line.strip() for line in f if line.strip()]

        # csv marker list
        if suffix == ".csv":
            df = pd.read_csv(input_path)

            if "marker" in df.columns:
                return df["marker"].dropna().astype(str).tolist()

            return df.iloc[:, 0].dropna().astype(str).tolist()

    raise ValueError(f"Unsupported input: {input_path}")