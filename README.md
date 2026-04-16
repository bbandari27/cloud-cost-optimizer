# Cloud Cost Optimizer using Airflow + Snowflake

Built a FinOps-focused data pipeline that ingests cloud cost data, detects underutilized resources, loads curated optimization data into Snowflake, and generates actionable savings reports.

## Tech Stack
- Apache Airflow
- Python
- Snowflake
- Pandas
- Docker Compose

## Architecture
1. Ingest raw cloud billing / usage data
2. Transform records and calculate waste cost
3. Load curated optimization output into Snowflake
4. Generate a final savings report

## Project Structure
```text
cloud-cost-optimizer-airflow-snowflake/
├── dags/
├── jobs/
├── data/
├── sql/
├── config/
├── requirements.txt
├── docker-compose.yml
└── README.md
```

## Local Run (without Airflow first)
```bash
python jobs/ingest_cost_data.py
python jobs/transform_cost_data.py
python jobs/generate_report.py
```

Load to Snowflake after adding `.env`:
```bash
python jobs/load_to_snowflake.py
```

## Airflow Run
```bash
docker compose up
```

Open Airflow UI at:
- http://localhost:8080

## Snowflake Setup
Copy `config/.env.example` to `.env` and fill your Snowflake credentials.

## Sample Output
The pipeline writes:
- `data/processed/optimized_cost_data.csv`
- `data/reports/final_report.txt`
