from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime
from psycopg2 import sql
import pandas as pd
import os

from utils.etl_utils import create_filepath, transform_appointments, transform_patients, load_appointments, load_patients

with DAG(
    "etl",
    tags=["healthcare_provider_etl"],
    start_date=datetime(2024, 1, 1),
    schedule_interval='*/10 * * * *',
    catchup=False,
) as dag:
    
    def extract(**kwargs):
        execution_date = kwargs['execution_date'].strftime('%Y-%m-%d %H:%M:%S')
        prev_execution_date = kwargs['prev_execution_date'].strftime('%Y-%m-%d %H:%M:%S')
        hook = PostgresHook(postgres_conn_id="healthcare_provider_oltp_conn")
        conn = hook.get_conn()
        cursor = conn.cursor()


        tables_query = """SELECT table_schema, table_name FROM information_schema.tables
                          WHERE table_schema NOT IN ('pg_catalog', 'information_schema') AND table_type = 'BASE TABLE';"""
        
        cursor.execute(tables_query)
        rows = cursor.fetchall()
        tables = [row[1] for row in rows]

        
        for table_name in tables:

            if execution_date == prev_execution_date:
                query = sql.SQL("""SELECT * FROM {table_name} 
                                   WHERE last_updated <= %(execution_date)s;"""
                                ).format(table_name = sql.Identifier(table_name))
                
            else:
                query = sql.SQL("""SELECT * FROM {table_name} 
                                   WHERE last_updated BETWEEN %(prev_execution_date)s AND %(execution_date)s;"""
                                ).format(table_name = sql.Identifier(table_name))

            cursor.execute(query, {'execution_date': execution_date, 'prev_execution_date': prev_execution_date, 'table_name': table_name})
            rows = cursor.fetchall()

            df = pd.DataFrame(rows)
            path = create_filepath(kwargs, table_name, "extract")
            df.to_csv(path, index=False, header=False)
        
        cursor.close()

        return tables
    

    extract_task = PythonOperator(
        task_id = 'extract_task',
        python_callable=extract
    )

    def transform(**kwargs):
        pat_path = create_filepath(kwargs, "patients", "extract")
        app_path = create_filepath(kwargs, "appointments", "extract")

        pat_df = transform_patients(pat_path)
        app_df = transform_appointments(app_path)

        transformed_pat_path = create_filepath(kwargs, "patients", "transform")
        transformed_app_path = create_filepath(kwargs, "appointments", "transform")

        pat_df.to_csv(transformed_pat_path, index=False, header=False)
        app_df.to_csv(transformed_app_path, index=False, header=False)

    transform_task = PythonOperator(
        task_id = 'transform_task',
        python_callable=transform
    )


    def load(**kwargs):
        pat_path = create_filepath(kwargs, "patients", "transform")
        app_path = create_filepath(kwargs, "appointments", "transform")

        load_appointments(app_path)
        load_patients(pat_path)

    load_task = PythonOperator(
        task_id = 'load_task',
        python_callable = load
    )

    extract_task >> transform_task >> load_task
    