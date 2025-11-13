import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = os.getenv("POSTGRES_URL")
if not POSTGRES_URL:
    raise RuntimeError("POSTGRES_URL not set in .env")

engine = create_engine(POSTGRES_URL)

def load_table(df, table_name):
    """Load a dataframe into PostgreSQL, replacing if exists"""
    print(f"Loading {len(df)} rows into {table_name}...")
    with engine.begin() as conn:
        pass
    print(f"✅ {table_name} loaded successfully")

if __name__ == "__main__":
    # Load crashes
    df_crashes = pd.read_csv("data/raw/data_raw_collisions.csv")
    load_table(df_crashes, "raw_collisions")

    # Load vehicles
    df_vehicles = pd.read_csv("data/raw/data_raw_vehicles.csv")
    load_table(df_vehicles, "raw_collision_vehicles")

    # Load persons
    df_persons = pd.read_csv("data/raw/data_raw_persons.csv")
    load_table(df_persons, "raw_collision_persons")
