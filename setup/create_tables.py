def create_oltp_tables(oltp_conn):

    oltp_conn.autocommit = True
    cursor = oltp_conn.cursor()

    oltp_query = """DROP TABLE IF EXISTS appointments;
                    DROP TABLE IF EXISTS patients;
                    DROP TABLE IF EXISTS staff;
                    DROP TABLE IF EXISTS departments;
                    CREATE TABLE departments (
                        department_id SERIAL PRIMARY KEY,
                        last_updated TIMESTAMP,
                        department_name VARCHAR(30)
                        );
                    CREATE TABLE staff (
                        staff_id SERIAL PRIMARY KEY,
                        last_updated TIMESTAMP,
                        first_name VARCHAR(30),
                        last_name VARCHAR(30),
                        phone_number BIGINT,
                        role VARCHAR(30),
                        department_id INT,
                        position VARCHAR(30)
                        );
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
                    CREATE TABLE appointments (
                        appointment_id SERIAL PRIMARY KEY,
                        last_updated TIMESTAMP,
                        appointment_date TIMESTAMP,
                        appointment_status VARCHAR,
                        patient_id INT,
                        staff_id INT,
                        notes VARCHAR
                        );"""
    cursor.execute(oltp_query)

    print("oltp tables created successfully ✅")

    cursor.close()


def create_olap_tables(olap_conn):

    olap_conn.autocommit = True
    cursor = olap_conn.cursor()

    olap_drop_query = """DROP TABLE IF EXISTS staging_appointments;
                         DROP TABLE IF EXISTS staging_patients;
                         DROP TABLE IF EXISTS staging_staff;
                         DROP TABLE IF EXISTS staging_departments;
                         DROP TABLE IF EXISTS fact_appointments;
                         DROP TABLE IF EXISTS dim_patients;
                         DROP TABLE IF EXISTS dim_staff;
                         DROP TABLE IF EXISTS dim_departments;"""

    cursor.execute(olap_drop_query)

    olap_create_query = """CREATE TABLE staging_departments (
                            department_id INT,
                            last_updated TIMESTAMP,
                            department_name VARCHAR(30)
                            );
                           CREATE TABLE staging_staff (
                            staff_id INT,
                            last_updated TIMESTAMP,
                            first_name VARCHAR(30),
                            last_name VARCHAR(30),
                            phone_number BIGINT,
                            role VARCHAR(30),
                            department_id INT,
                            position VARCHAR(30)
                           );
                            CREATE TABLE staging_patients (
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
                           CREATE TABLE dim_departments (
                            department_id INT PRIMARY KEY,
                            last_updated TIMESTAMP,
                            department_name VARCHAR(30)
                            );
                           CREATE TABLE dim_staff (
                            staff_id INT PRIMARY KEY,
                            last_updated TIMESTAMP,
                            first_name VARCHAR(30),
                            last_name VARCHAR(30),
                            phone_number BIGINT,
                            role VARCHAR(30),
                            department_id INT,
                            position VARCHAR(30)
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

    print("olap tables created successfully ✅")

    cursor.close()
