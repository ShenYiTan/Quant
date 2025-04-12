import requests
import pandas as pd
from datetime import datetime, timezone
import time
import functools
from dotenv import load_dotenv
import os

# Load the environment variables from .env.local
load_dotenv(".env.local")

# Get the API key
api_key = os.getenv("API_KEY")

# --- Configuration ---
begin_time = time.time()
start_date = datetime(2020, 4, 2, 15, 20, 0, tzinfo=timezone.utc)
start_time = timestamp_ms = int(start_date.timestamp() * 1000)
end_date = datetime(2023, 4, 2, 16, 21, 0, tzinfo=timezone.utc)
end_time = timestamp_ms = int(end_date.timestamp() * 1000)
# api_key = "PfIqrLdRgmmABukq1PC3PxRwf3LtnFvxNmQ5xN1fDRv4fFeS"  # API key
# actual base URL
base_url = "https://api.datasource.cybotrade.rs"

# --- Endpoint to Fetch Historical Data ---
# Replace with the correct endpoint
endpoint = f"{base_url}/cryptoquant/btc/market-data/price-ohlcv?window=hour"

# --- Headers (if required by the API) ---
headers = {
    "X-API-KEY": api_key,  # or "X-API-KEY": api_key if required
    "Accept": "application/json"
}

# --- Parameters ---
params = {
    # "symbol": symbol,
    # "interval": "1d",  # or whatever the API supports
    # "range": "1y",      # specify the range you need
    "start_time": start_time,  # "000000T000000",
    "end_time": end_time,
    # "limit":"200",
    # "flatten": "true"
}

# --- Make the API Request ---


@functools.lru_cache
def get_data():
    response = requests.get(endpoint, headers=headers, params=params)
    return response


# --- Check for successful response ---
if get_data().status_code == 200:
    data = get_data().json()
    print("API call successful!")

    # --- Assuming the response contains 'data' key for historical data ---
    # Adjust based on actual response structure
    df = pd.DataFrame(data["data"])

    # --- Convert date column if necessary ---
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

    # --- Display sample data ---
    # print(json.dumps(data, indent=2))
    finish_time = time.time()
    duration = finish_time - begin_time
    df.to_csv("sample_data.csv")
    # df.to_json("price.json")
    print(df)
    print(f"Response time: {duration:.3f} seconds")
else:
    print(f"Error {get_data().status_code}: {get_data().text}")
