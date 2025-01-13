import os
import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from psycopg2 import sql


def create_filepath(kwargs, table_name, stage):
    time_partition = kwargs.get('execution_date').strftime("%Y/%m/%d/%H")
    filename = kwargs.get('execution_date').strftime("%Y-%m-%d_%H:%M:%S")
    path = f"/tmp/{stage}/{table_name}/{time_partition}/{filename}.csv"
    os.makedirs(os.path.dirname(path), exist_ok=True)

    return path

def transform_appointments(app_path):
    app_cols = ['appointment_id', 'last_updated', 'appointment_date', "appointment_status", "patient_id", "staff_id", "notes"]

    app_df = pd.read_csv(app_path, names=app_cols)

    app_df['appointment_status'] = app_df['appointment_status'].fillna('upcoming')
    app_df.loc[app_df['appointment_status'].isin(['pending', 'booked', 'scheduled']), 'appointment_status'] = 'upcoming'

    return app_df

def transform_patients(pat_path):
    pat_cols = ['last_updated', 'patient_id', 'first_name', 'last_name', 'date_of_birth', 'sex', 'height', 'weight', 'phone_number', 'address']

    pat_df = pd.read_csv(pat_path, names=pat_cols)

    sex_map = {'male': 'm', 'female': 'f'}

    pat_df['sex'] = pat_df['sex'].replace(sex_map)

    pat_df['weight_kg'] = pat_df['weight'].apply(lambda x: lbs_to_kg(x) if 'lbs' in x else int(x[:-2]))

    pat_df['height_cm'] = pat_df['height'].apply(lambda x: ft_to_cm(x) if '\'' in x else int(x[:-2]))
 
    pat_df['bmi'] = (pat_df['weight_kg'] / (pat_df['height_cm'] / 100) ** 2).round(1)

    pat_df.drop(inplace=True, columns=['height', 'weight'])

    return pat_df

def lbs_to_kg(lbs):
    return int(int(lbs[:-3]) * 0.45359237)

def ft_to_cm(ft):
    ft_to_inches = int(ft[0]) * 12
    inches = int(ft.split("'")[1][:-1])
    return int((ft_to_inches + inches) * 2.54)

def load_patients(pat_path):
    hook = PostgresHook(postgres_conn_id="healthcare_provider_olap_conn")
    conn = hook.get_conn()
    cursor = conn.cursor()
    
    staging_query = sql.SQL("COPY staging_patients FROM {} WITH (FORMAT csv);").format(
        sql.Literal(pat_path)
    )

    cursor.execute(staging_query)

    upsert_query = """INSERT INTO dim_patients (last_updated, patient_id, first_name, last_name, date_of_birth, sex, height_cm, weight_kg, phone_number, address, bmi)
                      SELECT last_updated, patient_id, first_name, last_name, date_of_birth, sex, height_cm, weight_kg, phone_number, address, bmi
                      FROM staging_patients
                      ON CONFLICT(patient_id)
                      DO UPDATE SET
                        last_updated = EXCLUDED.last_updated,
                        height_cm = EXCLUDED.height_cm,
                        weight_kg = EXCLUDED.weight_kg,
                        last_name = EXCLUDED.last_name,
                        address = EXCLUDED.address,
                        bmi = EXCLUDED.bmi;
                      TRUNCATE TABLE staging_patients;"""

    cursor.execute(upsert_query)

    conn.commit()
    cursor.close()

def load_appointments(app_path):
    hook = PostgresHook(postgres_conn_id="healthcare_provider_olap_conn")
    conn = hook.get_conn()
    cursor = conn.cursor()

    staging_query = sql.SQL("COPY staging_appointments FROM {} WITH (FORMAT csv);").format(
        sql.Literal(app_path)
    )    

    cursor.execute(staging_query)

    upsert_query = """INSERT INTO fact_appointments (appointment_id, last_updated, appointment_date, appointment_status, patient_id, staff_id, notes)
                      SELECT appointment_id, last_updated, appointment_date, appointment_status, patient_id, staff_id, notes
                      FROM staging_appointments
                      ON CONFLICT(appointment_id)
                      DO UPDATE SET
                        last_updated = EXCLUDED.last_updated,
                        appointment_status = EXCLUDED.appointment_status,
                        appointment_date = EXCLUDED.appointment_date;
                      TRUNCATE TABLE staging_appointments;"""
    
    cursor.execute(upsert_query)

    conn.commit()
    cursor.close()

def upload_to_s3(path, stage, BUCKET_SUFFIX):
    stripped_path = path[5:]
    bucket_name = f"healthcare-provider-etl-{stage}-bucket-{BUCKET_SUFFIX}"
    s3_hook = S3Hook(aws_conn_id="healthcare_provider_aws_conn")
    s3_hook.load_file(filename=path, key = stripped_path, bucket_name=bucket_name, replace=True)
    print(f"uploaded to {stage} bucket!")