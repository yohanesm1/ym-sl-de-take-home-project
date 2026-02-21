import sys
import subprocess
import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URL = os.getenv("POSTGRES_URL")
if not POSTGRES_URL:
    raise RuntimeError("POSTGRES_URL not set in .env")

engine = create_engine(POSTGRES_URL)

# Step 1: Extract
print("\n" + "="*70)
print("Step 1: EXTRACT - Fetching data from NYC Open Data API")
print("="*70)
subprocess.run([sys.executable, "extract/fetch_collisions.py"], check=True)

# Step 2: Load
print("\n" + "="*70)
print("Step 2: LOAD - Loading raw data into PostgreSQL")
print("="*70)
subprocess.run([sys.executable, "load/load_to_postgres.py"], check=True)

# Step 3: Transform
print("\n" + "="*70)
print("Step 3: TRANSFORM - Creating analytical tables")
print("="*70)

# Run collision transformations
print("\nRunning collision transformations...")
with open("transform/transform_collisions.sql") as f:
    sql = f.read()

statements = [s.strip() for s in sql.split(";") if s.strip()]

with engine.begin() as conn:
    for stmt in statements:
        conn.execute(text(stmt))

print("Collision tables created")




print("\n" + "="*70)
print("ELT PIPELINE COMPLETED SUCCESSFULLY!")
print("="*70)
print("\nNext steps:")
print("  • Run: jupyter notebook analyze_collisions.ipynb")
print("  • Or query tables directly from PostgreSQL")
print("="*70 + "\n")