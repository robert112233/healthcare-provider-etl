import os
import psycopg2
from dotenv import load_dotenv


def create_connection(db, RDS_ENDPOINT):
    load_dotenv()
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    OLTP_NAME = os.getenv("OLTP_NAME")
    OLAP_NAME = os.getenv("OLAP_NAME")
    if None in [DB_USERNAME, DB_PASSWORD, OLTP_NAME, OLAP_NAME]:
        print("\nMissing environment variable, "
              "check they have been set correctly in .env 📄")

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
