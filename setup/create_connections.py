from build_local import build_local_oltp, build_local_olap
from airflow.models import Connection
from airflow.utils.session import create_session

def create_oltp_connection(ENVIRONMENT):
 
    with create_session() as session:

        conn = session.query(Connection).filter(Connection.conn_id == 'healthcare_provider_oltp_conn').first()

        if conn:
            session.delete(conn)
            session.commit()

        conn = Connection(
            conn_id='healthcare_provider_oltp_conn',
            conn_type='postgres',
            host='localhost',
            login='postgres',
            password='postgres',
            extra={"database": "healthcare_provider_oltp"},
            port=5432
            )


        session.add(conn)
        session.commit()

        print("Added 'healthcare_provider_oltp_conn' to Airflow connections 🔌")

def create_olap_connection(ENVIRONMENT):

    with create_session() as session:

        conn = session.query(Connection).filter(Connection.conn_id == 'healthcare_provider_olap_conn').first()

        if conn:
            session.delete(conn)
            session.commit()

        conn = Connection(
            conn_id='healthcare_provider_olap_conn',
            conn_type='postgres',
            host='localhost',
            login='postgres',
            password='postgres',
            extra={"database": "healthcare_provider_olap"},
            port=5432
            )


        session.add(conn)
        session.commit()

        print("Added 'healthcare_provider_olap_conn' to Airflow connections 🔌")