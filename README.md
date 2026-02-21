# NYC Motor Vehicle Collision ELT Pipeline

This project builds a mini ELT pipeline using NYC Open Data Motor Vehicle Collision records. The pipeline extracts raw collision data from the NYC Open Data API, loads it into PostgreSQL, transforms it into analytics-ready tables, and explores insights through a Jupyter notebook.

The goal of the project is not just correctness, but to demonstrate how I think about data modeling, transformations, and analytical usability.

---

## Tech Stack

- Python (requests, pandas, sqlalchemy)
- PostgreSQL
- SQL (transformations)
- Jupyter Notebook (analysis and visualization)
- NYC Open Data API

---

Setup Instructions:

1. Clone the repository

git clone <repo-url>
cd ym-sl-de-take-home-project

2. Create and activate a virtual environment

python -m venv .venv
source .venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Set up PostgreSQL

createdb nyc_collisions

Create a .env file in the project root:

POSTGRES_URL=postgresql://<user>@localhost:5432/nyc_collisions
Running the Pipeline

# Run the full ELT pipeline:

python main.py

This will:

Extract recent NYC collision data from the API

Load raw data into PostgreSQL (raw schema)

Transform data into analytics tables (analytics schema)


Roughly How Long Did This Project Take?

2.5 hours total.

How I Felt About the Project & Challenges Faced

The project was fine to me clear request to pull the data and be able to show tables and visualizations, noticed as I built I had to go back and add to more to previous step as certain data became more relevant.