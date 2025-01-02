import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
import sys
from build_local import build_local_oltp, build_local_olap
from create_connections import create_oltp_connection, create_olap_connection
from airflow.models import Connection
from airflow.utils.session import create_session

def setup():
    choice = input("Where would you like to provision the infracture? (local or cloud)\n")

    if choice in ['local', 'cloud']:
        with open(".env", "w") as f:
            f.write(f"ENVIRONMENT={choice}\n")
    else: 
        setup()

    load_dotenv()
    ENVIRONMENT = os.getenv('ENVIRONMENT')

    provision_databases(ENVIRONMENT)
    create_connection(ENVIRONMENT)



def provision_databases(ENVIRONMENT):
    if ENVIRONMENT == 'local':
        print('\nSetting up DBs locally...\n')
        build_local_oltp()
        build_local_olap()

def create_connection(ENVIRONMENT):
    if ENVIRONMENT == 'local':
        print("\nCreating Airflow connection locally...\n")
    create_olap_connection(ENVIRONMENT)
    create_oltp_connection(ENVIRONMENT)

    




setup()

