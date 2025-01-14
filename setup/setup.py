import requests
import psycopg2
import subprocess
import os
from dotenv import load_dotenv
from build_local import build_oltp, build_olap
from create_connections import create_airflow_oltp_connection, create_airflow_olap_connection, create_airflow_aws_connection
from create_tables import create_oltp_tables, create_olap_tables
from create_and_insert_data import insert_patients, insert_appointments
from datetime import datetime
from requests.auth import HTTPBasicAuth
from psycopg2.errors import ObjectInUse, DuplicateDatabase

def setup():
    safety_check = input("This will destroy all databases, are you sure? (yes or no)\n")

    if safety_check not in ['YES', "yes"]:
        if safety_check not in ['NO', "no"]:
            print("\nInvalid answer, aborting...\n")
        return

    ENVIRONMENT = input("\nWhere would you like to provision the infracture? (local or cloud)\n")

    if ENVIRONMENT not in ['local', 'cloud']:
        setup()

    store_env_var("ENVIRONMENT", ENVIRONMENT)

    if ENVIRONMENT == 'local':
        os.environ["AIRFLOW__CORE__DAGS_FOLDER"] = os.path.join(os.getcwd(), "DAGs")

    RDS_ENDPOINT = 'localhost'
    MWAA_ENDPOINT = 'http://localhost:8081'

    if ENVIRONMENT == 'cloud':
        RDS_ENDPOINT, BUCKET_SUFFIX, S3_IAM_ACCESS_KEY_ID, S3_IAM_SECRET_ACCESS_KEY, MWAA_ENDPOINT = apply_terraform()
        store_env_var("BUCKET_SUFFIX", BUCKET_SUFFIX)
        store_env_var("S3_IAM_ACCESS_KEY_ID", S3_IAM_ACCESS_KEY_ID)
        store_env_var("S3_IAM_SECRET_ACCESS_KEY", S3_IAM_SECRET_ACCESS_KEY)
        create_airflow_aws_connection(MWAA_ENDPOINT)
  
    postgres_conn = create_connection("postgres", RDS_ENDPOINT)

    provision_databases(postgres_conn)
    
    oltp_conn = create_connection("oltp", RDS_ENDPOINT)
    olap_conn = create_connection("olap", RDS_ENDPOINT)

    create_airflow_connection(RDS_ENDPOINT, MWAA_ENDPOINT)
    create_tables(oltp_conn, olap_conn)
    create_and_insert_data(oltp_conn)
    trigger_update_appointments(MWAA_ENDPOINT)
    trigger_etl(MWAA_ENDPOINT)
   
        

def create_connection(db, RDS_ENDPOINT):
    load_dotenv()
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    OLTP_NAME = os.getenv("OLTP_NAME")
    OLAP_NAME = os.getenv("OLAP_NAME")

    dbname = 'postgres'

    if db == "oltp":
        dbname=OLTP_NAME
    elif db == "olap":
        dbname=OLAP_NAME

    HOSTNAME = RDS_ENDPOINT.split(':')[0]

    connection = psycopg2.connect(
        dbname=dbname,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=HOSTNAME,
        port=5432
    )
    return connection


def provision_databases(postgres_conn):
            build_oltp(postgres_conn)
            build_olap(postgres_conn)


def create_airflow_connection(RDS_ENDPOINT, MWAA_ENDPOINT):
    create_airflow_olap_connection(RDS_ENDPOINT, MWAA_ENDPOINT)
    create_airflow_oltp_connection(RDS_ENDPOINT, MWAA_ENDPOINT)

def create_tables(oltp_conn, olap_conn):
    print("\nCreating tables... \n")
    create_oltp_tables(oltp_conn)
    create_olap_tables(olap_conn)

def create_and_insert_data(oltp_conn):
    print("\nCreating and inserting patient and appointment data... \n")
    insert_patients(oltp_conn)
    insert_appointments(oltp_conn)

def trigger_update_appointments(MWAA_ENDPOINT):
    url = f"http://{MWAA_ENDPOINT}/api/v1/dags/update_appointments"
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "is_paused": False
    }

    auth = HTTPBasicAuth('admin', 'admin')
    response = requests.patch(url, json=payload, headers=headers, auth=auth)
    if response.status_code == 200:
        print(f"\nDAG 'update_appointments' has been successfully unpaused. 🔧")
    else:
        print(response.text)

def trigger_etl(MWAA_ENDPOINT):
    url = f"http://{MWAA_ENDPOINT}/api/v1/dags/etl"
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "is_paused": False
    }

    auth = HTTPBasicAuth('admin', 'admin')
    response = requests.patch(url, json=payload, headers=headers, auth=auth)
    if response.status_code == 200:
        print(f"\nDAG 'etl' has been successfully unpaused. 🔧")
        if MWAA_ENDPOINT == "http://localhost:8081":
            print(f"\nThe first ingestion will soon be complete, check the /tmp folder and connect to local healthcare_provider_olap db to see loaded data ")
        else:
            print("\nThe first ingestion will soon be complete, check the s3 buckets and healthcare_provider_olap RDS to see loaded data")
    else:
        print(response.text)

def apply_terraform():
    print("\nApplying terraform, this will take at least 5 minutes 🏗️")
    subprocess.run(['bash', '-c', './setup/cloud_setup.sh'])
    print('\nApplied!')
    result = subprocess.run(['bash', '-c', './setup/cloud_output.sh'], capture_output=True, text=True, check=True)
    return result.stdout.strip().split('\n')


def store_env_var(key, value):
    with open('.env', 'r') as file:
        content = file.readlines()
        
    env_var_found = False
    for i, line in enumerate(content):
        if line.startswith(f"{key}="):
            if line.strip() != f"{key}={value}":
                content[i] = f"{key}={value}\n"
            env_var_found = True
            break

    if not env_var_found:
        content.append(f"\n{key}={value}")

    with open('.env', 'w') as file:
        file.writelines(content)

setup()