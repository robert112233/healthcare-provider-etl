from exceptions import (
    AuthException, DagNotFoundException)
import requests
from requests.auth import HTTPBasicAuth


def trigger_update_appointments(MWAA_ENDPOINT):
    print("triggering update appointments...")
    url = f"http://{MWAA_ENDPOINT}/api/v1/dags/update_appointments"
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "is_paused": False
    }
    auth = HTTPBasicAuth('admin', 'admin')
    try:
        response = requests.patch(url, json=payload, headers=headers,
                                  auth=auth, timeout=3)
        if response.status_code == 401:
            raise AuthException
        elif response.status_code == 404:
            raise DagNotFoundException
    except requests.exceptions.Timeout:
        print("\nDAG 'update_appointments' has been successfully unpaused. 🔧")


def trigger_etl(MWAA_ENDPOINT):
    print("triggering ETL...")
    url = f"http://{MWAA_ENDPOINT}/api/v1/dags/etl"
    headers = {
        "Content-Type": "application/json",
    }
    payload = {
        "is_paused": False
    }

    auth = HTTPBasicAuth('admin', 'admin')
    try:
        response = requests.patch(url, json=payload, headers=headers,
                                  auth=auth, timeout=3)
        if response.status_code == 401:
            raise AuthException
    except requests.exceptions.Timeout:
        print("\nDAG 'etl' has been successfully unpaused. 🔧")
        if MWAA_ENDPOINT == "http://127.0.0.1:8080":
            print("\nThe first ingestion will soon be complete, "
                  "check the /tmp folder and connect to "
                  "local healthcare_provider_olap db to see loaded data")
        else:
            print("\nThe first ingestion will soon be complete, "
                  "check the s3 buckets "
                  "and healthcare_provider_olap RDS to see loaded data")
