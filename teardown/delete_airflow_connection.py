import requests


def delete_airflow_connection(MWAA_ENDPOINT, conn_name):
    delete_url = f'http://{MWAA_ENDPOINT}/api/v1/connections/{conn_name}'

    response = requests.delete(delete_url, auth=('admin', 'admin'))

    if response.status_code == 404:
        print(f"{conn_name} doesn't exist! Skipping ⏩")
    else:
        print(f"Deleted '{conn_name}' from Airflow connections 🔌")
