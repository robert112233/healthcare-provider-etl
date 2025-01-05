import requests
import psycopg2
import subprocess
import os
from dotenv import load_dotenv
from build_local import build_oltp, build_olap
from create_connections import create_airflow_oltp_connection, create_airflow_olap_connection
from create_tables import create_oltp_tables, create_olap_tables
from create_and_insert_data import insert_patients, insert_appointments
from datetime import datetime
from requests.auth import HTTPBasicAuth
from psycopg2.errors import ObjectInUse

def setup():
    safety_check = input("This will destroy all databases, are you sure? (yes or no)\n")

    if safety_check not in ['YES', "yes"]:
        if safety_check not in ['NO', "no"]:
            print("\nInvalid answer, aborting...\n")
        return

    ENVIRONMENT = input("\nWhere would you like to provision the infracture? (local or cloud)\n")

    if ENVIRONMENT not in ['local', 'cloud']:
        setup()

    store_environment(ENVIRONMENT)

    if ENVIRONMENT == 'local':
        os.environ["AIRFLOW__CORE__DAGS_FOLDER"] = os.path.join(os.getcwd(), "DAGs")

    RDS_ENDPOINT = 'localhost'

    if ENVIRONMENT == 'cloud':
        RDS_ENDPOINT = apply_terraform()

    postgres_conn = create_connection("postgres", RDS_ENDPOINT)

    try:
        provision_databases(postgres_conn)
    except ObjectInUse: 
        print("You are still connected to either of the databases outside the project somewhere, aborting ❌")

    oltp_conn = create_connection("oltp", RDS_ENDPOINT)
    olap_conn = create_connection("olap", RDS_ENDPOINT)

    create_airflow_connection(RDS_ENDPOINT)
    create_tables(oltp_conn, olap_conn)
    create_and_insert_data(oltp_conn)
    trigger_update_appointments(RDS_ENDPOINT)
    trigger_etl(RDS_ENDPOINT)
   
        

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
         

    connection = psycopg2.connect(
        dbname=dbname,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=RDS_ENDPOINT,
        port=5432
    )

    return connection


def provision_databases(postgres_conn):
        try:
            build_oltp(postgres_conn)
            build_olap(postgres_conn)
        except ObjectInUse:
           raise ObjectInUse

def create_airflow_connection(RDS_ENDPOINT):
    create_airflow_olap_connection(RDS_ENDPOINT)
    create_airflow_oltp_connection(RDS_ENDPOINT)

def create_tables(oltp_conn, olap_conn):
    print("\nCreating tables locally... \n")
    create_oltp_tables(oltp_conn)
    create_olap_tables(olap_conn)

def create_and_insert_data(oltp_conn):
    print("\nCreating and inserting patient and appointment data locally... \n")
    insert_patients(oltp_conn)
    insert_appointments(oltp_conn)

def trigger_update_appointments(RDS_ENDPOINT):
    url = f"http://{RDS_ENDPOINT}:8081/api/v1/dags/update_appointments"
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

def trigger_etl(RDS_ENDPOINT):
    url = f"http://{RDS_ENDPOINT}:8081/api/v1/dags/etl"
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
        if RDS_ENDPOINT == "localhost":
            print(f"\nThe first ingestion will soon be complete, check the /tmp folder and connect to local healthcare_provider_olap db to see loaded data ")
        else:
            print("\nThe first ingestion will soon be complete, check the s3 buckets and healthcare_provider_olap RDS to see loaded data")
    else:
        print(response.text)

def apply_terraform():
    result = subprocess.run(['bash', '-c', './setup/cloud_setup.sh'], capture_output=True, text=True)
    return result.stdout

def store_environment(ENVIRONMENT):
    with open('../.env', 'r') as file:
            content = file.read()
            if f"ENVIRONMENT={ENVIRONMENT}" in content:
                return
    with open('../.env', 'a') as file:
        file.write(f'\nENVIRONMENT={ENVIRONMENT}')


setup()

