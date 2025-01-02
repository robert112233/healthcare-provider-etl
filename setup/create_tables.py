import logging
import psycopg2

def create_oltp_tables(ENVIRONMENT):
    connection = psycopg2.connect(
            dbname="healthcare_provider_oltp",
            user="postgres",
            password="postgres",
            host='localhost',
            port=5432
        )
        
    connection.autocommit = True
    cursor = connection.cursor()

    oltp_query = """DROP TABLE IF EXISTS patients;
                    DROP TABLE IF EXISTS appointments;
                    CREATE TABLE patients (
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
                        );
                    CREATE TABLE IF NOT EXISTS appointments (
                        appointment_id SERIAL PRIMARY KEY,
                        last_updated TIMESTAMP,
                        appointment_date TIMESTAMP,
                        appointment_status VARCHAR,
                        patient_id INT, 
                        staff_id INT,
                        notes VARCHAR
                        );"""
    cursor.execute(oltp_query)

    print(f"oltp tables created successfully ✅")

    cursor.close()
    connection.close()

def create_olap_tables(ENVIRONMENT):
    connection = psycopg2.connect(
            dbname="healthcare_provider_oltp",
            user="postgres",
            password="postgres",
            host='localhost',
            port=5432
        )
        
    connection.autocommit = True
    cursor = connection.cursor()

    olap_drop_query = """DROP TABLE IF EXISTS staging_patients;
                         DROP TABLE IF EXISTS staging_appointments;
                         DROP TABLE IF EXISTS dim_patients;
                         DROP TABLE IF EXISTS fact_appointments;"""

    cursor.execute(olap_drop_query)

    olap_create_query = """CREATE TABLE staging_patients (
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
                            );
                           CREATE TABLE staging_appointments (
                            appointment_id INT,
                            last_updated TIMESTAMP,
                            appointment_date TIMESTAMP,
                            appointment_status VARCHAR,
                            patient_id INT, 
                            staff_id INT,
                            notes VARCHAR
                            );
                           CREATE TABLE dim_patients (
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
                            );
                           CREATE TABLE fact_appointments (
                            appointment_id INT PRIMARY KEY,
                            last_updated TIMESTAMP,
                            appointment_date TIMESTAMP,
                            appointment_status VARCHAR,
                            patient_id INT, 
                            staff_id INT,
                            notes VARCHAR
                            );"""

    cursor.execute(olap_create_query)

    print(f"olap tables created successfully ✅")

    cursor.close()
    connection.close()
