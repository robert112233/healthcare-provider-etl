import requests


def delete_airflow_connection(MWAA_ENDPOINT, conn_name):
    delete_url = f'http://{MWAA_ENDPOINT}/api/v1/connections/{conn_name}'

    requests.delete(delete_url, auth=('admin', 'admin'))

    print(f"Deleted '{conn_name}' from Airflow connections 🔌")
