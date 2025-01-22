import os
import requests
from dotenv import load_dotenv
from requests.exceptions import ConnectionError


def create_airflow_oltp_connection(RDS_ENDPOINT, MWAA_ENDPOINT):

    load_dotenv()

    try:
        DB_USERNAME = os.getenv("DB_USERNAME")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        HOSTNAME = RDS_ENDPOINT.split(":")[0]

        conn_name = "healthcare_provider_oltp_conn"
        post = f'http://{MWAA_ENDPOINT}/api/v1/connections'
        json = {"connection_id": conn_name,
                "conn_type": "postgres",
                "host": HOSTNAME,
                "login": DB_USERNAME,
                "password": DB_PASSWORD,
                "extra": '{"dbname": "healthcare_provider_oltp"}',
                "port": 5432
                }
        requests.post(post, json=json, auth=('admin', 'admin'))
        print("Added 'healthcare_provider_oltp_conn' to Airflow connections 🔌")
    except ConnectionError:
        raise ConnectionError


def create_airflow_olap_connection(RDS_ENDPOINT, MWAA_ENDPOINT):
    try:
        load_dotenv()

        DB_USERNAME = os.getenv("DB_USERNAME")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        HOSTNAME = RDS_ENDPOINT.split(":")[0]

        conn_name = "healthcare_provider_olap_conn"
        post_url = f'http://{MWAA_ENDPOINT}/api/v1/connections'
        json = {"connection_id": conn_name,
                "conn_type": "postgres",
                "host": HOSTNAME,
                "login": DB_USERNAME,
                "password": DB_PASSWORD,
                "extra": '{"dbname": "healthcare_provider_olap"}',
                "port": 5432
                }
        requests.post(post_url, json=json, auth=('admin', 'admin'))
        print(
            "\nAdded 'healthcare_provider_olap_conn' to Airflow connections 🔌"
             )
    except ConnectionError:
        raise ConnectionError


def create_airflow_aws_connection(MWAA_ENDPOINT):

    try:
        load_dotenv()

        S3_IAM_ACCESS_KEY_ID = os.getenv("S3_IAM_ACCESS_KEY_ID")
        S3_IAM_SECRET_ACCESS_KEY = os.getenv("S3_IAM_SECRET_ACCESS_KEY")
        conn_name = 'healthcare_provider_aws_conn'
        post = f'http://{MWAA_ENDPOINT}/api/v1/connections'
        json = {"connection_id": conn_name,
                "conn_type": "aws",
                "login": S3_IAM_ACCESS_KEY_ID,
                "password": S3_IAM_SECRET_ACCESS_KEY,
                }
        requests.post(post, json=json, auth=('admin', 'admin'))

        print("Added 'healthcare_provider_aws_conn' to Airflow connections 🔌")
    except ConnectionError:
        raise ConnectionError
