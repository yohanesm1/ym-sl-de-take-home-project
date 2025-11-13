import requests
import pandas as pd


# API endpoints for NYC Motor Vehicle Collisions
CRASH_COLLISION_ID = 'h9gi-nx95'
CRASH_VEHICLE_ID = 'bm4k-52h4'
CRASH_PERSONS_ID = 'f55k-p6yu'

#fetch data from NYC Open Data API on all crashes for 2024
def fetch_data(id, name, limit=100000):
    print(f"Fetching {name} from NYC Open Data...")
    url = (
        f"https://data.cityofnewyork.us/resource/{id}.json"
        f"?$limit={limit}"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    df = pd.DataFrame(resp.json())
    return df

if __name__ == "__main__":
    pass