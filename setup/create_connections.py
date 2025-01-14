from airflow.models import Connection
from airflow.utils.session import create_session
from dotenv import load_dotenv
import os
import requests

def create_airflow_oltp_connection(RDS_ENDPOINT, MWAA_ENDPOINT):

    load_dotenv()

    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    HOSTNAME = RDS_ENDPOINT.split(":")[0]

    patch_url = f'{MWAA_ENDPOINT}/api/v1/connections/healthcare_provider_oltp_conn'
    post_url = f'{MWAA_ENDPOINT}/api/v1/connections'
    json = {"connection_id": "healthcare_provider_oltp_conn",
            "conn_type": "postgres",
            "host": HOSTNAME,
            "login": DB_USERNAME,
            "password": DB_PASSWORD,
            "extra": '{"dbname": "healthcare_provider_oltp"}',
            "port": 5432
            }
    response = requests.patch(patch_url, json=json, auth=('admin', 'admin'))
    if response.status_code == 404:
        requests.post(post_url, json=json, auth=('admin', 'admin'))

    print("Added 'healthcare_provider_oltp_conn' to Airflow connections 🔌")

def create_airflow_olap_connection(RDS_ENDPOINT, MWAA_ENDPOINT):

    load_dotenv()

    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    HOSTNAME = RDS_ENDPOINT.split(":")[0]

    patch_url = f'{MWAA_ENDPOINT}/api/v1/connections/healthcare_provider_olap_conn'
    post_url = f'{MWAA_ENDPOINT}/api/v1/connections'
    json = {"connection_id": "healthcare_provider_olap_conn",
            "conn_type": "postgres",
            "host": HOSTNAME,
            "login": DB_USERNAME,
            "password": DB_PASSWORD,
            "extra": '{"dbname": "healthcare_provider_olap"}',
            "port": 5432
            }
    response = requests.patch(patch_url, json=json, auth=('admin', 'admin'))
    if response.status_code == 404:
        requests.post(post_url, json=json, auth=('admin', 'admin'))

    print("Added 'healthcare_provider_olap_conn' to Airflow connections 🔌")

def create_airflow_aws_connection(MWAA_ENDPOINT):

    load_dotenv()

    S3_IAM_ACCESS_KEY_ID = os.getenv("S3_IAM_ACCESS_KEY_ID")
    S3_IAM_SECRET_ACCESS_KEY = os.getenv("S3_IAM_SECRET_ACCESS_KEY")


    patch_url = f'{MWAA_ENDPOINT}/api/v1/connections/healthcare_provider_aws_conn'
    post_url = f'{MWAA_ENDPOINT}/api/v1/connections'
    json = {"connection_id": "healthcare_provider_aws_conn",
            "conn_type": "aws",
            "login": S3_IAM_ACCESS_KEY_ID,
            "password": S3_IAM_SECRET_ACCESS_KEY,
            }
    response = requests.patch(patch_url, json=json, auth=('admin', 'admin'))
    if response.status_code == 404:
        requests.post(post_url, json=json, auth=('admin', 'admin'))

    print("Added 'healthcare_provider_aws_conn' to Airflow connections 🔌")
