import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
import sys

def build_local_oltp():
    connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host='localhost',
            port=5432
        )
        
    connection.autocommit = True
    cursor = connection.cursor()

    drop_oltp_query = "DROP DATABASE IF EXISTS healthcare_provider_oltp;"
    cursor.execute(drop_oltp_query)

    create_oltp_query = "CREATE DATABASE healthcare_provider_oltp;"
    cursor.execute(create_oltp_query)
    print(f"Database 'healthcare_provider_oltp' created successfully 💿")

    cursor.close()
    connection.close()

def build_local_olap():
    connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host='localhost',
            port=5432
        )
        
    connection.autocommit = True
    cursor = connection.cursor()

    drop_oltp_query = "DROP DATABASE IF EXISTS healthcare_provider_olap;"
    cursor.execute(drop_oltp_query)

    create_oltp_query = "CREATE DATABASE healthcare_provider_olap;"
    cursor.execute(create_oltp_query)
    print(f"Database 'healthcare_provider_olap' created successfully 💿")

    cursor.close()
    connection.close()