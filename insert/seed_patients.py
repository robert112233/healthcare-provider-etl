from get_connection import get_connection
from create_random_patients import create_random_patients

def seed_patients():
    drop_patients_table()
    create_patients_table()
    insert_patients()

def drop_patients_table():
    connection = get_connection()
    connection.run("""DROP TABLE IF EXISTS patients;""")
    print('patients table dropped 🫳')


def create_patients_table():
    connection = get_connection()
    connection.run("""CREATE TABLE IF NOT EXISTS patients (
                   patient_id SERIAL PRIMARY KEY,
                   first_name VARCHAR(30),
                   last_name VARCHAR(30),
                   date_of_birth DATE,
                   phone_number BIGINT, 
                   address VARCHAR
                   );""")
    print('patients table created ✅')


def insert_patients():
    patients = create_random_patients() 
    connection = get_connection()
    query = """INSERT INTO patients (first_name, last_name, date_of_birth, phone_number, address)
                           VALUES (:first_name, :last_name, :date_of_birth, :phone_number, :address)"""
    for patient in patients:
        connection.run(query, **patient)
    
    print('inserted patients ✅')