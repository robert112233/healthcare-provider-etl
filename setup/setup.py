import os
from dotenv import load_dotenv
from build_local import build_local_oltp, build_local_olap
from create_connections import create_oltp_connection, create_olap_connection
from create_tables import create_oltp_tables, create_olap_tables
from create_and_insert_data import insert_patients, insert_appointments

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
    create_tables(ENVIRONMENT)
    create_and_insert_data(ENVIRONMENT)

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

def create_tables(ENVIRONMENT):
    print("\nCreating tables locally... \n")
    create_oltp_tables(ENVIRONMENT)
    create_olap_tables(ENVIRONMENT)

def create_and_insert_data(ENVIRONMENT):
    print("\nCreating and inserting patient and appointment data locally... \n")
    insert_patients(ENVIRONMENT)
    insert_appointments(ENVIRONMENT)

setup()

