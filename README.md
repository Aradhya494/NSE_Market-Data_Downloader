# NSE Market Data Downloader

A Python command-line application that downloads four market datasets from the
official National Stock Exchange of India (NSE) website and stores them in
separate CSV files.

## Features

- Downloads Top Gainers and Losers, Upper Band Hitters, Volume Gainers, and 52-Week High.
- Saves each dataset to its own CSV file in `output/`.
- Offers an interactive menu or a command-line dataset option.
- Validates downloaded data before saving.
- Handles network errors, timeouts, HTTP errors, invalid JSON, and empty responses.
- Logs successful and failed downloads in `logs/app.log`.
- Avoids duplicate stock rows when the same dataset is downloaded more than once on the same day.
- Includes basic automated tests using pytest.

## Requirements

- Python 3.10 or later
- Internet connection

## Setup on Windows

1. Install Python from https://www.python.org/downloads/ and select **Add Python to PATH** during installation.
2. Extract the project ZIP.
3. Open the extracted `nse_market_data_downloader` folder in Visual Studio Code.
4. In VS Code, select **Terminal > New Terminal**.
5. Run:

   ```bash
   py -m venv .venv
   .venv\Scripts\activate
   py -m pip install -r requirements.txt
   ```

## Run the application

Interactive menu:

```bash
py main.py
```

Download all four datasets:

```bash
py main.py --dataset all
```

Download one dataset:

```bash
py main.py --dataset gainers_losers
py main.py --dataset upper_band
py main.py --dataset volume_gainers
py main.py --dataset 52_week_high
```

## Output files

The application creates these files:

- `output/top_gainers_losers.csv`
- `output/upper_band_hitters.csv`
- `output/volume_gainers.csv`
- `output/52_week_high.csv`
- `logs/app.log`

Each CSV includes a `download_date` column.

## Run tests

```bash
py -m pytest -v
```

## Important note about NSE availability

The downloader uses JSON endpoints called by the official NSE website. NSE may
temporarily block automated requests, return an empty dataset outside market
hours, or change its website/API response. The application reports these
conditions in the terminal and log file rather than silently saving invalid data.
Use a reasonable request rate and comply with NSE website terms and access rules.
