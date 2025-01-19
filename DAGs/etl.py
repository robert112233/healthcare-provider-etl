import os
import dotenv
import logging
import pandas as pd
from airflow import DAG
from io import StringIO
from psycopg2 import sql
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from utils.etl_utils import (
    create_filepath,
    transform_appointments,
    transform_patients,
    transform_staff,
    transform_departments,
    load_appointments,
    load_patients,
    load_staff,
    load_departments,
    upload_to_s3
)

with DAG(
    "etl",
    tags=["healthcare_provider_etl"],
    start_date=datetime(2024, 1, 1),
    schedule_interval='*/20 * * * *',
    catchup=False,
) as dag:

    def extract(**kwargs):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        print("extracting...")
        exec_date = kwargs['next_execution_date'].strftime('%Y-%m-%d %H:%M:%S')
        prev_exec_date = kwargs['execution_date'].strftime('%Y-%m-%d %H:%M:%S')
        hook = PostgresHook(postgres_conn_id="healthcare_provider_oltp_conn")
        conn = hook.get_conn()
        cursor = conn.cursor()

        tables_query = """
        SELECT table_schema, table_name FROM information_schema.tables
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
        AND table_type = 'BASE TABLE';
        """

        cursor.execute(tables_query)
        rows = cursor.fetchall()
        tables = [row[1] for row in rows]

        dotenv.load_dotenv()

        ENVIRONMENT = os.getenv("ENVIRONMENT")
        BUCKET_SUFFIX = os.getenv("BUCKET_SUFFIX")

        for table in tables:

            if exec_date == prev_exec_date:
                print("\nIt's the first run, ingesting everything...")
                query = sql.SQL("""SELECT * FROM {table}
                                   WHERE last_updated <= %(exec_date)s;"""
                                ).format(table=sql.Identifier(table))

            else:
                query = sql.SQL(
                    """
                    SELECT * FROM {table}
                    WHERE last_updated
                    BETWEEN %(prev_exec_date)s AND %(exec_date)s;
                    """
                    ).format(table=sql.Identifier(table))

            params = {'exec_date': exec_date,
                      'prev_exec_date': prev_exec_date,
                      'table': table}

            cursor.execute(query, params)
            rows = cursor.fetchall()
            print(f"\nExtracted {len(rows)} rows from {table}")

            df = pd.DataFrame(rows)
            path = create_filepath(kwargs, table, "extract")

            if ENVIRONMENT == 'local':
                df.to_csv(path, index=False, header=False)
            if ENVIRONMENT == 'cloud':
                csv_buffer = StringIO()
                df.to_csv(csv_buffer, index=False, header=False)
                upload_to_s3(csv_buffer, path, 'extract', BUCKET_SUFFIX)

        cursor.close()

    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract
    )

    def transform(**kwargs):
        dep_path = create_filepath(kwargs, "departments", "extract")
        staff_path = create_filepath(kwargs, "staff", "extract")
        pat_path = create_filepath(kwargs, "patients", "extract")
        app_path = create_filepath(kwargs, "appointments", "extract")

        dep_df = transform_departments(dep_path)
        staff_df = transform_staff(staff_path)
        pat_df = transform_patients(pat_path)
        app_df = transform_appointments(app_path)

        trans_dep_path = create_filepath(kwargs, "departments", "transform")
        trans_staff_path = create_filepath(kwargs, "staff", "transform")
        trans_pat_path = create_filepath(kwargs, "patients", "transform")
        trans_app_path = create_filepath(kwargs, "appointments", "transform")

        dep_df.to_csv(trans_dep_path, index=False, header=False)
        staff_df.to_csv(trans_staff_path, index=False, header=False)
        pat_df.to_csv(trans_pat_path, index=False, header=False)
        app_df.to_csv(trans_app_path, index=False, header=False)

    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform
    )

    def load(**kwargs):
        dep_path = create_filepath(kwargs, "departments", "transform")
        staff_path = create_filepath(kwargs, "staff", "transform")
        pat_path = create_filepath(kwargs, "patients", "transform")
        app_path = create_filepath(kwargs, "appointments", "transform")

        load_departments(dep_path)
        load_staff(staff_path)
        load_patients(pat_path)
        load_appointments(app_path)


    load_task = PythonOperator(
        task_id='load_task',
        python_callable=load
    )

    extract_task >> transform_task >> load_task
