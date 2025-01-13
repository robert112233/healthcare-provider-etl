import requests
import os
from dotenv import load_dotenv

def create_airflow_aws_connection():

    load_dotenv()

    S3_IAM_ACCESS_KEY_ID = os.getenv("S3_IAM_ACCESS_KEY_ID")
    S3_IAM_SECRET_ACCESS_KEY = os.getenv("S3_IAM_SECRET_ACCESS_KEY")


    patch_url = 'http://localhost:8081/api/v1/connections/healthcare_provider_aws_conn'
    post_url = 'http://localhost:8081/api/v1/connections'
    json = {"connection_id": "healthcare_provider_aws_conn",
            "conn_type": "aws",
            "login": S3_IAM_ACCESS_KEY_ID,
            "password": S3_IAM_SECRET_ACCESS_KEY,
            }
    response = requests.patch(patch_url, json=json, auth=('admin', 'admin'))
    if response.status_code == 404:
        requests.post(post_url, json=json, auth=('admin', 'admin'))

    print("Added 'healthcare_provider_aws_conn' to Airflow connections 🔌")

create_airflow_aws_connection()


