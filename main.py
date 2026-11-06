import argparse
import logging
from pathlib import Path

from config import DATASETS, OUTPUT_DIR, LOG_DIR
from downloader import NSEDownloader, DownloadError
from storage import save_dataset
from validator import validate_dataframe, ValidationError

def setup_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_DIR / "app.log", encoding="utf-8"),
            logging.StreamHandler()
        ],
        force=True,
    )

def choose_dataset():
    print("\nNSE MARKET DATA DOWNLOADER")
    print("1. Top Gainers and Losers")
    print("2. Upper Circuit / Upper Band Hitters")
    print("3. Volume Gainers")
    print("4. 52-Week High")
    print("5. Download ALL datasets")
    choice = input("\nEnter your choice (1-5): ").strip()
    mapping = {
        "1": "gainers_losers",
        "2": "upper_band",
        "3": "volume_gainers",
        "4": "52_week_high",
        "5": "all",
    }
    return mapping.get(choice)

def run_download(dataset_name):
    downloader = NSEDownloader()
    selected = list(DATASETS.keys()) if dataset_name == "all" else [dataset_name]
    success_count = 0

    for name in selected:
        try:
            logging.info("Starting download: %s", name)
            dataframe = downloader.download(name)
            validate_dataframe(dataframe, name)
            output_path = save_dataset(dataframe, name, OUTPUT_DIR)
            logging.info("SUCCESS: %s | %s records | saved to %s",
                         name, len(dataframe), output_path)
            print(f"SUCCESS: {name} - {len(dataframe)} records saved.")
            success_count += 1
        except (DownloadError, ValidationError, ValueError) as exc:
            logging.exception("FAILED: %s | %s", name, exc)
            print(f"FAILED: {name} - {exc}")
        except Exception as exc:
            logging.exception("Unexpected error while downloading %s", name)
            print(f"UNEXPECTED ERROR: {name} - {exc}")

    print(f"\nCompleted: {success_count}/{len(selected)} dataset(s) downloaded.")
    print(f"CSV files: {OUTPUT_DIR.resolve()}")
    print(f"Logs: {(LOG_DIR / 'app.log').resolve()}")

def main():
    parser = argparse.ArgumentParser(description="Download NSE market datasets into CSV files.")
    parser.add_argument(
        "--dataset",
        choices=[*DATASETS.keys(), "all"],
        help="Dataset to download. Omit this option to use the interactive menu."
    )
    args = parser.parse_args()

    setup_logging()
    dataset_name = args.dataset or choose_dataset()
    if not dataset_name:
        print("Invalid choice. Please run the application again and enter 1-5.")
        return

    run_download(dataset_name)

if __name__ == "__main__":
    main()
