from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime
import logging

logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

with DAG(
    "reset_db",
    tags=["healthcare_provider_etl"],
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    drop_patients_table_task = PostgresOperator(
        task_id='reset_db',
        postgres_conn_id='healthcare_provider_olap_conn', 
        sql="""DROP TABLE IF EXISTS staging_patients;
               DROP TABLE IF EXISTS staging_appointments;
               DROP TABLE IF EXISTS dim_patients;
               DROP TABLE IF EXISTS fact_appointments;""",
    )