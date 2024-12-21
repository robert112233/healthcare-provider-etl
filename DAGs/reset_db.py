from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime
import logging

logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

with DAG(
    "reset_db",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    create_patients_table_task = PostgresOperator(
        task_id='reset_db',
        postgres_conn_id='my_postgres_conn', 
        sql="""DROP TABLE IF EXISTS patients;
               DROP TABLE IF EXISTS appointments;""",
    )