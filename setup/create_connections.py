from airflow.models import Connection
from airflow.utils.session import create_session
from dotenv import load_dotenv
import os

def create_airflow_oltp_connection(RDS_ENDPOINT):
 
    with create_session() as session:

        conn = session.query(Connection).filter(Connection.conn_id == 'healthcare_provider_oltp_conn').first()

        if conn:
            session.delete(conn)
            session.commit()

        load_dotenv()

        DB_USERNAME = os.getenv("DB_USERNAME")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        OLTP_NAME = os.getenv("OLTP_NAME")

        conn = Connection(
            conn_id='healthcare_provider_oltp_conn',
            conn_type='postgres',
            host=RDS_ENDPOINT,
            login=DB_USERNAME,
            password=DB_PASSWORD,
            extra={"dbname": OLTP_NAME},
            port=5432
            )

        session.add(conn)
        session.commit()

        print("Added 'healthcare_provider_oltp_conn' to Airflow connections 🔌")

def create_airflow_olap_connection(RDS_ENDPOINT):

    with create_session() as session:

        conn = session.query(Connection).filter(Connection.conn_id == 'healthcare_provider_olap_conn').first()

        if conn:
            session.delete(conn)
            session.commit()

        load_dotenv()

        DB_USERNAME = os.getenv("DB_USERNAME")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        OLAP_NAME = os.getenv("OLAP_NAME")

        conn = Connection(
            conn_id='healthcare_provider_olap_conn',
            conn_type='postgres',
            host=RDS_ENDPOINT,
            login=DB_USERNAME,
            password=DB_PASSWORD,
            extra={"dbname": OLAP_NAME},
            port=5432
            )


        session.add(conn)
        session.commit()

        print("Added 'healthcare_provider_olap_conn' to Airflow connections 🔌")