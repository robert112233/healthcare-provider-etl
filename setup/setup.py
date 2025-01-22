import os
from store_env_var import store_env_var
from get_mwaa_token import get_mwaa_token
from apply_terraform import apply_terraform
from create_connection import create_connection
from exceptions import (
    MissingEnvsException, AuthException, DagNotFoundException)
from build_local import build_oltp, build_olap
from requests.exceptions import ConnectionError
from create_tables import create_oltp_tables, create_olap_tables
from trigger_dags import trigger_etl, trigger_update_appointments
from create_and_insert_data import insert_patients, insert_appointments, insert_departments, insert_staff
from create_airflow_connections import (
    create_airflow_oltp_connection, create_airflow_olap_connection)


def setup():
    prompt = "This will destroy all tables, are you sure? (yes or no)\n"
    safety_check = input(prompt)

    if safety_check not in ['YES', "yes"]:
        if safety_check not in ['NO', "no"]:
            print("\nInvalid answer, aborting...\n")
        return

    ENVIRONMENT = input("\nWhere would you like to "
    "provision the infracture? (local or cloud)\n"
                        )

    if ENVIRONMENT not in ['local', 'cloud']:
        setup()

    store_env_var("ENVIRONMENT", ENVIRONMENT)

    if ENVIRONMENT == 'local':
        os.environ["AIRFLOW__CORE__DAGS_FOLDER"] = os.path.join(
            os.getcwd(), "DAGs"
        )

    RDS_ENDPOINT = '127.0.0.1'
    MWAA_ENDPOINT = '127.0.0.1:8080'

    try:
        if ENVIRONMENT == 'cloud':
            (
              RDS_ENDPOINT,
              BUCKET_SUFFIX,
              S3_IAM_ACCESS_KEY_ID,
              S3_IAM_SECRET_ACCESS_KEY,
              MWAA_ENDPOINT
            ) = apply_terraform()
            store_env_var("BUCKET_SUFFIX", BUCKET_SUFFIX)
            store_env_var("S3_IAM_ACCESS_KEY_ID", S3_IAM_ACCESS_KEY_ID)
            store_env_var("S3_IAM_SECRET_ACCESS_KEY", S3_IAM_SECRET_ACCESS_KEY)

        store_env_var("RDS_ENDPOINT", RDS_ENDPOINT)
        store_env_var("MWAA_ENDPOINT", MWAA_ENDPOINT)
        get_mwaa_token()

        postgres_conn = create_connection("postgres", RDS_ENDPOINT)

        provision_databases(postgres_conn)


        oltp_conn = create_connection("oltp", RDS_ENDPOINT)
        olap_conn = create_connection("olap", RDS_ENDPOINT)


        create_airflow_connection(RDS_ENDPOINT, MWAA_ENDPOINT)
        create_tables(oltp_conn, olap_conn)
        create_and_insert_data(oltp_conn)

        trigger_update_appointments(MWAA_ENDPOINT)
        trigger_etl(MWAA_ENDPOINT)

    except ConnectionError:
        print("\nConnection error, "
              "make sure the webserver & scheduler are running! 🎛️")
    except MissingEnvsException:
        print("\nMissing environment variable, "
              "check they have been set correctly in .env 📄")
    except AuthException:
        print("\nNot authenticated to use the Airflow API, "
              "make sure to create an admin user (step 5 in the README) 🛂")
    except DagNotFoundException:
        print("\nThe script can't locate a dag, "
              "make sure to export the DAG path (step 4 in the README) 🔎")


def provision_databases(postgres_conn):
    build_oltp(postgres_conn)
    build_olap(postgres_conn)


def create_airflow_connection(RDS_ENDPOINT, MWAA_ENDPOINT):
    try:
        create_airflow_oltp_connection(RDS_ENDPOINT, MWAA_ENDPOINT)
        create_airflow_olap_connection(RDS_ENDPOINT, MWAA_ENDPOINT)
    except ConnectionError:
        raise ConnectionError


def create_tables(oltp_conn, olap_conn):
    print("\nCreating tables... \n")
    create_oltp_tables(oltp_conn)
    create_olap_tables(olap_conn)


def create_and_insert_data(oltp_conn):
    print("\nCreating and inserting data... \n")
    insert_departments(oltp_conn)
    insert_staff(oltp_conn)
    insert_patients(oltp_conn)
    insert_appointments(oltp_conn)

setup()
