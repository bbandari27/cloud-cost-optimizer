from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

from jobs.ingest_cost_data import ingest_cost_data
from jobs.transform_cost_data import transform_cost_data
from jobs.load_to_snowflake import load_to_snowflake
from jobs.generate_report import generate_report

default_args = {
    "owner": "bhavya",
    "start_date": datetime(2026, 1, 1),
    "retries": 1,
}

with DAG(
    dag_id="cloud_cost_optimization_pipeline",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
    description="FinOps pipeline using Airflow and Snowflake",
) as dag:

    ingest_task = PythonOperator(
        task_id="ingest_cost_data",
        python_callable=ingest_cost_data,
    )

    transform_task = PythonOperator(
        task_id="transform_cost_data",
        python_callable=transform_cost_data,
    )

    load_task = PythonOperator(
        task_id="load_to_snowflake",
        python_callable=load_to_snowflake,
    )

    report_task = PythonOperator(
        task_id="generate_report",
        python_callable=generate_report,
    )

    ingest_task >> transform_task >> load_task >> report_task
