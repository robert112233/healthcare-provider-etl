from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime
from utils.create_and_insert_utils import create_random_patients, create_random_appointment
import logging
from random import randint

logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

with DAG(
    "update_appointments",
    tags=["healthcare_provider_etl"],
    start_date=datetime(2024, 1, 1),
    schedule_interval="*/7 * * * *",
    catchup=False,
) as dag:

    def update_appointments():
        amount = randint(0, 5)
        hook = PostgresHook(postgres_conn_id="healthcare_provider_oltp_conn")
        conn = hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(appointment_id) FROM appointments;")
        max_id = cursor.fetchone()[0]

        for _ in range(amount):
            random_id = randint(1, max_id)
            random_status = ['cancelled', 'attended', 'missed'][randint(0,2)]
            cursor.execute("""UPDATE appointments 
                              SET appointment_status = %(random_status)s, last_updated = NOW() 
                              WHERE appointment_id = %(random_id)s AND appointment_status IN ('upcoming', 'pending', 'booked', 'scheduled');""", {'random_status': random_status, 'random_id': random_id})
            logger.info(f'Appointment with id of {random_id} has been updated to {random_status}')

        conn.commit()
        cursor.close()

    def insert_random_appointments():
        amount = randint(0, 5)
        hook = PostgresHook(postgres_conn_id="healthcare_provider_oltp_conn")
        conn = hook.get_conn()
        cursor = conn.cursor()
        for _ in range(amount):
            appointment_values = create_random_appointment()
            logger.info(appointment_values)
            cursor.execute("""INSERT INTO appointments (last_updated, appointment_date, appointment_status, patient_id, staff_id, notes) 
                              VALUES
                              (%(last_updated)s, %(appointment_date)s, %(appointment_status)s, %(patient_id)s, %(staff_id)s, %(notes)s);""", appointment_values)
        
        conn.commit()
        cursor.close()
    

    update_appointments_task = PythonOperator(
        task_id = 'update_appointment_task',
        python_callable=update_appointments
        )
    
    insert_random_appointments_task = PythonOperator(
        task_id = 'insert_random_appointments',
        python_callable=insert_random_appointments
    )
    
    update_appointments_task >> insert_random_appointments_task
