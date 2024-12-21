from get_connection import get_connection
from create_random_appointment import create_random_appointment
from create_random_patients import create_random_patients
import datetime

def seed_appointments():
    drop_appointments_table()
    create_appointments_table

def drop_appointments_table():
    connection = get_connection()
    connection.run("""DROP TABLE IF EXISTS appointments;""")
    print('appointments table dropped 🫳')

def create_appointments_table():
    connection = get_connection()
    connection.run("""CREATE TABLE IF NOT EXISTS appointments (
                   appointment_id SERIAL PRIMARY KEY,
                   last_updated TIMESTAMP,
                   appointment_date TIMESTAMP,
                   appointment_status VARCHAR,
                   patient_id INT, 
                   staff_id INT,
                   notes VARCHAR
                   );""")
    print('appointments table created ✅')
    
seed_appointments()