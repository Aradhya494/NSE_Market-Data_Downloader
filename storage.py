from datetime import datetime
from pathlib import Path
import pandas as pd

from config import DATASETS

def save_dataset(dataframe: pd.DataFrame, dataset_name: str, output_dir: Path) -> Path:
    """Append new rows, while preventing duplicate stock rows for the same day."""
    if dataset_name not in DATASETS:
        raise ValueError(f"Unknown dataset: {dataset_name}")

    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / DATASETS[dataset_name]["filename"]

    new_data = dataframe.copy()
    today = datetime.now().strftime("%Y-%m-%d")
    new_data["download_date"] = today

    if file_path.exists():
        old_data = pd.read_csv(file_path)
        combined = pd.concat([old_data, new_data], ignore_index=True, sort=False)
    else:
        combined = new_data

    # Use available identifier columns to remove duplicates from same-day reruns.
    identifier = next(
        (col for col in combined.columns
         if str(col).strip().lower() in {"symbol", "underlying"}),
        None
    )
    if identifier:
        dedupe_columns = ["download_date", identifier]
        if "category" in combined.columns:
            dedupe_columns.append("category")
        combined = combined.drop_duplicates(subset=dedupe_columns, keep="last")
    else:
        combined = combined.drop_duplicates(keep="last")

    # Write to a temporary file first to avoid leaving a half-written CSV.
    temp_path = file_path.with_suffix(".tmp")
    combined.to_csv(temp_path, index=False, encoding="utf-8")
    temp_path.replace(file_path)
    return file_path
