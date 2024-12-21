from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime
from utils.create_and_insert_utils import create_random_patients, create_random_appointments
import logging

logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

with DAG(
    "create_and_insert_data",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    create_patients_table_task = PostgresOperator(
        task_id='create_patients_table',
        postgres_conn_id='my_postgres_conn', 
        sql="""CREATE TABLE IF NOT EXISTS patients (
                   last_updated TIMESTAMP,
                   patient_id SERIAL PRIMARY KEY,
                   first_name VARCHAR(30),
                   last_name VARCHAR(30),
                   date_of_birth DATE,
                   sex VARCHAR(15),
                   height VARCHAR(15),
                   weight VARCHAR(15),
                   phone_number BIGINT, 
                   address VARCHAR
                   );""",
    )

    create_appointments_table_task = PostgresOperator(
        task_id = 'create_appointments_table',
        postgres_conn_id='my_postgres_conn',
        sql="""CREATE TABLE IF NOT EXISTS appointments (
                   appointment_id SERIAL PRIMARY KEY,
                   last_updated TIMESTAMP,
                   appointment_date TIMESTAMP,
                   appointment_status VARCHAR,
                   patient_id INT, 
                   staff_id INT,
                   notes VARCHAR
                   );"""
    )

    def insert_patients():
        hook = PostgresHook(postgres_conn_id="my_postgres_conn")
        conn = hook.get_conn()
        cursor = conn.cursor()
        patients = create_random_patients() 
        query = """
        INSERT INTO patients (last_updated, first_name, last_name, date_of_birth, sex, height, weight, phone_number, address)
        VALUES (%(last_updated)s, %(first_name)s, %(last_name)s, %(date_of_birth)s, %(sex)s, %(height)s, %(weight)s, %(phone_number)s, %(address)s);
        """
        for patient in patients:
            cursor.execute(query, patient)
        logger.info(f"Successfully inserted {len(patients)} patients ✅")
        conn.commit()
        cursor.close()

    insert_patients_task = PythonOperator(
        task_id = 'insert_patients_task',
        python_callable=insert_patients
    )

    def insert_appointments():
        appointments = create_random_appointments()
        hook = PostgresHook(postgres_conn_id="my_postgres_conn")
        conn = hook.get_conn()
        cursor = conn.cursor()
        query = """INSERT INTO appointments (last_updated, appointment_date, appointment_status, patient_id, staff_id, notes) 
                      VALUES
                      (%(last_updated)s, %(appointment_date)s, %(appointment_status)s, %(patient_id)s, %(staff_id)s, %(notes)s);"""
        for appointment in appointments:
            cursor.execute(query, appointment)
        logger.info(f"Successfully inserted {len(appointments)} appointments ✅")

        conn.commit()
        cursor.close()
    
    insert_appointments_task = PythonOperator(
        task_id = 'insert_appointments_task',
        python_callable=insert_appointments
    )

    create_patients_table_task >> create_appointments_table_task >> insert_patients_task >> insert_appointments_task



