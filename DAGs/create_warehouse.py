from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime
import logging

logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

with DAG(
    "create_warehouse",
    tags=["healthcare_provider_etl"],
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:
    
    create_patients_staging_task = PostgresOperator(
        task_id = 'create_patients_staging',
        postgres_conn_id='olap_conn',
        sql="""CREATE TABLE IF NOT EXISTS staging_patients (
                   last_updated TIMESTAMP,
                   patient_id INT,
                   first_name VARCHAR(30),
                   last_name VARCHAR(30),
                   date_of_birth DATE,
                   sex VARCHAR(15),
                   phone_number BIGINT, 
                   address VARCHAR,
                   weight_kg VARCHAR(15),
                   height_cm VARCHAR(15),
                   bmi FLOAT
                   )""")
    
    create_appointments_staging_task = PostgresOperator(
        task_id = 'create_appointments_staging',
        postgres_conn_id='olap_conn',
        sql="""CREATE TABLE IF NOT EXISTS staging_appointments (
                   appointment_id INT,
                   last_updated TIMESTAMP,
                   appointment_date TIMESTAMP,
                   appointment_status VARCHAR,
                   patient_id INT, 
                   staff_id INT,
                   notes VARCHAR
                   )"""
    )
    
    create_patients_table_task = PostgresOperator(
        task_id = 'create_patients_table',
        postgres_conn_id='olap_conn',
        sql="""CREATE TABLE IF NOT EXISTS dim_patients (
                   last_updated TIMESTAMP,
                   patient_id INT PRIMARY KEY,
                   first_name VARCHAR(30),
                   last_name VARCHAR(30),
                   date_of_birth DATE,
                   sex VARCHAR(15),
                   phone_number BIGINT, 
                   address VARCHAR,
                   weight_kg VARCHAR(15),
                   height_cm VARCHAR(15),
                   bmi FLOAT
                   )""")
    
    create_appointments_table_task = PostgresOperator(
        task_id = 'create_appointments_table',
        postgres_conn_id='olap_conn',
        sql="""CREATE TABLE IF NOT EXISTS fact_appointments (
                   appointment_id INT PRIMARY KEY,
                   last_updated TIMESTAMP,
                   appointment_date TIMESTAMP,
                   appointment_status VARCHAR,
                   patient_id INT, 
                   staff_id INT,
                   notes VARCHAR
                   )"""
    )

    create_patients_staging_task >> create_patients_table_task >> create_appointments_staging_task >> create_appointments_table_task