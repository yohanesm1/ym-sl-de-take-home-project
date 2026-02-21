# load/load_to_postgres.py
import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = os.getenv("POSTGRES_URL")
if not POSTGRES_URL:
    raise RuntimeError("POSTGRES_URL not set in .env")

engine = create_engine(POSTGRES_URL)

RAW_DIR = Path("data/raw")

FILES = {
    "collision_crashes": RAW_DIR / "collision_crashes.csv",
    "collision_vehicles": RAW_DIR / "collision_vehicles.csv",
    "collision_persons": RAW_DIR / "collision_persons.csv",
}

def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [
        c.strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace("/", "_")
        for c in df.columns
    ]
    return df

def load_table(df: pd.DataFrame, schema: str, table_name: str) -> None:
    """Load a dataframe into PostgreSQL, replacing if exists."""
    df = _normalize_columns(df)

    # Convert object columns that contain dict/list into JSON strings to avoid psycopg errors
    for col in df.columns:
        if df[col].dtype == "object":
            sample = df[col].dropna().head(50)
            if not sample.empty and sample.map(lambda x: isinstance(x, (dict, list))).any():
                df[col] = df[col].apply(lambda x: None if pd.isna(x) else (x if not isinstance(x, (dict, list)) else str(x)))

    print(f"Loading {len(df):,} rows into {schema}.{table_name}...")

    with engine.begin() as conn:
        conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema};"))

    # Replace table each run for idempotency
    df.to_sql(
        name=table_name,
        con=engine,
        schema=schema,
        if_exists="replace",
        index=False,
        chunksize=5000,
        method="multi",
    )

    # Verify counts
    with engine.begin() as conn:
        db_count = conn.execute(text(f"SELECT COUNT(*) FROM {schema}.{table_name};")).scalar_one()

    print(f"✅ {schema}.{table_name} loaded successfully (db rows: {db_count:,})")

def main():
    # Validate raw files exist
    missing = [str(p) for p in FILES.values() if not p.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing raw CSV file(s):\n  " + "\n  ".join(missing) +
            "\nRun: python extract/fetch_collisions.py"
        )

    df_crashes = pd.read_csv(FILES["collision_crashes"])
    load_table(df_crashes, schema="raw", table_name="collision_crashes")

    df_vehicles = pd.read_csv(FILES["collision_vehicles"])
    load_table(df_vehicles, schema="raw", table_name="collision_vehicles")

    df_persons = pd.read_csv(FILES["collision_persons"])
    load_table(df_persons, schema="raw", table_name="collision_persons")

if __name__ == "__main__":
    main()