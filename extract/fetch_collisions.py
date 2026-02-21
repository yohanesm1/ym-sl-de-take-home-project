import os
import time
from pathlib import Path

import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# NYC Open Data dataset IDs
CRASH_COLLISION_ID = "h9gi-nx95"  # Crashes
CRASH_VEHICLE_ID = "bm4k-52h4"    # Vehicles
CRASH_PERSONS_ID = "f55k-p6yu"    # Persons

BASE_URL = "https://data.cityofnewyork.us/resource"
DATA_DIR = Path(os.getenv("DATA_DIR", "data/raw"))
YEAR = os.getenv("YEAR", "2024")

SOCRATA_APP_TOKEN = os.getenv("SOCRATA_APP_TOKEN")  # optional

def fetch_data(dataset_id: str, name: str, page_size: int = 50000) -> pd.DataFrame:
    print(f"Fetching {name} from NYC Open Data...")

    headers = {}
    if SOCRATA_APP_TOKEN:
        headers["X-App-Token"] = SOCRATA_APP_TOKEN

    start = f"{YEAR}-01-01T00:00:00.000"
    end = f"{int(YEAR) + 1}-01-01T00:00:00.000"
    where_clause = f"crash_date >= '{start}' AND crash_date < '{end}'"

    all_rows = []
    offset = 0

    while True:
        params = {
            "$limit": page_size,
            "$offset": offset,
            "$where": where_clause,
        }
        url = f"{BASE_URL}/{dataset_id}.json"
        resp = requests.get(url, params=params, headers=headers, timeout=60)
        resp.raise_for_status()

        rows = resp.json()
        if not rows:
            break

        all_rows.extend(rows)
        offset += page_size

        print(f"  fetched {len(rows):,} rows (total {len(all_rows):,})")
        time.sleep(0.2)

    df = pd.DataFrame(all_rows)

    if not df.empty:
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    return df

def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    datasets = [
        (CRASH_COLLISION_ID, "collision_crashes", "collision_crashes.csv"),
        (CRASH_VEHICLE_ID, "collision_vehicles", "collision_vehicles.csv"),
        (CRASH_PERSONS_ID, "collision_persons", "collision_persons.csv"),
    ]

    for dataset_id, name, filename in datasets:
        df = fetch_data(dataset_id, name)
        out_path = DATA_DIR / filename
        df.to_csv(out_path, index=False)
        print(f"  wrote {len(df):,} rows to {out_path}")

if __name__ == "__main__":
    main()