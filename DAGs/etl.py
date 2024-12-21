from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime
from psycopg2 import sql
import logging
import pendulum

with DAG(
    "etl",
    start_date=datetime(2024, 1, 1),
    schedule_interval='*/1 * * * *',
    catchup=False,
) as dag:
    
    def extract(**kwargs):
        execution_date = kwargs['execution_date'].strftime('%Y-%m-%d %H:%M:%S')
        prev_execution_date = kwargs['prev_execution_date'].strftime('%Y-%m-%d %H:%M:%S')
        hook = PostgresHook(postgres_conn_id="my_postgres_conn")
        conn = hook.get_conn()
        cursor = conn.cursor()


        tables_query = """SELECT table_schema, table_name FROM information_schema.tables
                          WHERE table_schema NOT IN ('pg_catalog', 'information_schema') AND table_type = 'BASE TABLE';"""
        
        cursor.execute(tables_query)
        rows = cursor.fetchall()
        tables = [row[1] for row in rows]

        extracted_data = {}
        
        for table_name in tables:

            if execution_date == prev_execution_date:
                query = sql.SQL("""SELECT * FROM {table_name} 
                                   WHERE last_updated <= %(execution_date)s;"""
                                ).format(table_name = sql.Identifier(table_name))
                
                print("it's the first run!", prev_execution_date, execution_date)
            else:
                query = sql.SQL("""SELECT * FROM {table_name} 
                                   WHERE last_updated BETWEEN %(prev_execution_date)s AND %(execution_date)s;"""
                                ).format(table_name = sql.Identifier(table_name))
                
                print("it's not the first run", prev_execution_date, execution_date)

            cursor.execute(query, {'execution_date': execution_date, 'prev_execution_date': prev_execution_date, 'table_name': table_name})
            rows = cursor.fetchall()
            extracted_data[table_name] = rows
        
        cursor.close()
        
        return extracted_data



    extract_task = PythonOperator(
        task_id = 'extract_task',
        python_callable=extract
    )