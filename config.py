from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

NSE_HOME = "https://www.nseindia.com"

REQUEST_TIMEOUT = 25
REQUEST_DELAY_SECONDS = 1.5

DATASETS = {
    "gainers_losers": {
        "filename": "top_gainers_losers.csv",
        "requests": [
            {
                "endpoint": "/api/live-analysis-variations",
                "params": {"index": "gainers"},
                "category": "gainers"
            },
            {
                "endpoint": "/api/live-analysis-variations",
                "params": {"index": "loosers"},
                "category": "losers"
            }
        ]
    },

    "upper_band": {
        "filename": "upper_band_hitters.csv",
        "requests": [
            {
                "endpoint": "/api/live-analysis-price-band-hitter",
                "params": {},
                "category": None
            }
        ]
    },

    "volume_gainers": {
        "filename": "volume_gainers.csv",
        "requests": [
            {
                "endpoint": "/api/live-analysis-volume-gainers",
                "params": {},
                "category": None
            }
        ]
    },

    "52_week_high": {
        "filename": "52_week_high.csv",
        "requests": [
            {
                "endpoint": "/api/live-analysis-data-52weekhighstock",
                "params": {},
                "category": None
            }
        ]
    }
}