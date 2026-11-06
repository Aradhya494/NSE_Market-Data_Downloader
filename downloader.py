import logging
import time
import requests
import pandas as pd

from config import (
    NSE_HOME,
    DATASETS,
    REQUEST_TIMEOUT,
    REQUEST_DELAY_SECONDS
)


class DownloadError(Exception):
    """Custom error for NSE download failures."""


class NSEDownloader:

    def __init__(self):
        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/128.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Referer": NSE_HOME + "/",
            "Accept-Language": "en-US,en;q=0.9"
        })

    def _warm_up_session(self):
        try:
            response = self.session.get(
                NSE_HOME,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()

        except requests.RequestException as error:
            raise DownloadError(
                f"NSE connection failed: {error}"
            ) from error

    def _get_records(self, payload, dataset_name):

        records = []

        if isinstance(payload, list):
            records = payload

        elif isinstance(payload, dict):

            if dataset_name == "gainers_losers":

                for category, value in payload.items():

                    if isinstance(value, dict):
                        category_data = value.get("data")

                        if isinstance(category_data, list):
                            for item in category_data:
                                if isinstance(item, dict):
                                    item = item.copy()
                                    item["market_category"] = category
                                    records.append(item)

            else:
                data = payload.get("data")

                if isinstance(data, list):
                    records = data

                elif isinstance(data, dict):
                    nested = data.get("data")

                    if isinstance(nested, list):
                        records = nested

        if not records:
            logging.error(
                "Unexpected response: %s",
                str(payload)[:1000]
            )

            raise DownloadError(
                f"No usable records received for {dataset_name}"
            )

        return [
            item for item in records
            if isinstance(item, dict)
        ]

    def _fetch_data(self, endpoint, params, dataset_name):

        url = NSE_HOME + endpoint

        try:
            response = self.session.get(
                url,
                params=params,
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()

        except requests.Timeout as error:
            raise DownloadError(
                f"Request timed out: {endpoint}"
            ) from error

        except requests.RequestException as error:
            raise DownloadError(
                f"Request failed: {error}"
            ) from error

        try:
            payload = response.json()

        except ValueError as error:
            raise DownloadError(
                "NSE returned invalid JSON instead of data."
            ) from error

        return self._get_records(payload, dataset_name)

    def download(self, dataset_name):

        if dataset_name not in DATASETS:
            raise ValueError("Invalid dataset name")

        self._warm_up_session()

        all_records = []

        for request_info in DATASETS[dataset_name]["requests"]:

            records = self._fetch_data(
                request_info["endpoint"],
                request_info["params"],
                dataset_name
            )

            category = request_info.get("category")

            if category:
                for record in records:
                    record["category"] = category

            all_records.extend(records)

            time.sleep(REQUEST_DELAY_SECONDS)

        if not all_records:
            raise DownloadError("No records downloaded.")

        dataframe = pd.DataFrame(all_records)

        logging.info(
            "%s records downloaded for %s",
            len(dataframe),
            dataset_name
        )

        return dataframe