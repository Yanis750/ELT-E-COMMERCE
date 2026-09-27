from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "yanis",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="ecommerce_pipeline",
    description="Ingestion CSV -> transformation dbt -> tests de qualite",
    default_args=default_args,
    start_date=datetime(2026, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["ecommerce", "phase2"],
) as dag:

    load_raw_data = BashOperator(
        task_id="load_raw_data",
        bash_command="python /opt/airflow/ingestion/load_raw_data.py",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=(
            "cd /opt/airflow/dbt_project/ecommerce_dbt && "
            "dbt run --profiles-dir /opt/airflow/dbt_project"
        ),
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=(
            "cd /opt/airflow/dbt_project/ecommerce_dbt && "
            "dbt test --profiles-dir /opt/airflow/dbt_project"
        ),
    )

    load_raw_data >> dbt_run >> dbt_test
