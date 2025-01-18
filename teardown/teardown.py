import os
import psycopg2
import subprocess
from dotenv import load_dotenv
from requests.exceptions import ConnectionError
from psycopg2.errors import ObjectInUse, InvalidCatalogName
from delete_airflow_connection import delete_airflow_connection


def teardown():
    load_dotenv()

    ENVIRONMENT = os.getenv("ENVIRONMENT")
    RDS_ENDPOINT = os.getenv("RDS_ENDPOINT")
    MWAA_ENDPOINT = os.getenv("MWAA_ENDPOINT")

    try:
        delete_connections(MWAA_ENDPOINT)
        delete_dbs(RDS_ENDPOINT)

        if ENVIRONMENT == "cloud":
            subprocess.run(['bash', '-c', './setup/cloud_setup.sh'])
    except ConnectionError:
        print("""\nConnection error,
              make sure the webserver & scheduler are running! 🎛️""")


def delete_connections(MWAA_ENDPOINT):
    try:
        print("\n")
        oltp_conn = 'healthcare_provider_oltp_conn'
        olap_conn = 'healthcare_provider_olap_conn'
        aws_conn = 'healthcare_provider_aws_conn'
        delete_airflow_connection(MWAA_ENDPOINT, oltp_conn)
        delete_airflow_connection(MWAA_ENDPOINT, olap_conn)
        delete_airflow_connection(MWAA_ENDPOINT, aws_conn)
        print("\n")
    except ConnectionError:
        raise ConnectionError


def delete_dbs(RDS_ENDPOINT):
    postgres_conn = create_connection("postgres", RDS_ENDPOINT)

    postgres_conn.autocommit = True
    cursor = postgres_conn.cursor()

    try:
        create_oltp_query = "DROP DATABASE healthcare_provider_oltp;"
        cursor.execute(create_oltp_query)
        print("Database 'healthcare_provider_oltp' deleted successfully 🫳")

    except ObjectInUse:
        print("""You are still connected to healthcare_provider_oltp somewhere!
              Disconnect and try again""")
    except InvalidCatalogName:
        print("Database doesn't exist! Skipping ⏩")

    try:
        create_oltp_query = "DROP DATABASE healthcare_provider_olap;"
        cursor.execute(create_oltp_query)
        print("Database 'healthcare_provider_olap' deleted successfully 🫳")

    except ObjectInUse:
        print("""You are still connected to healthcare_provider_olap somewhere!
              Disconnect and try again""")
    except InvalidCatalogName:
        print("Database doesn't exist! Skipping ⏩")

    cursor.close()


def create_connection(db, RDS_ENDPOINT):
    load_dotenv()
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    OLTP_NAME = os.getenv("OLTP_NAME")
    OLAP_NAME = os.getenv("OLAP_NAME")

    dbname = 'postgres'

    if db == "oltp":
        dbname = OLTP_NAME
    elif db == "olap":
        dbname = OLAP_NAME

    HOSTNAME = RDS_ENDPOINT.split(':')[0]

    connection = psycopg2.connect(
        dbname=dbname,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=HOSTNAME,
        port=5432
    )
    return connection


teardown()
