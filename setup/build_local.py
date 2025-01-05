import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
import sys
from psycopg2.errors import ObjectInUse

def build_oltp(postgres_conn): 
    postgres_conn.autocommit = True
    cursor = postgres_conn.cursor()

    try:
        drop_oltp_query = "DROP DATABASE IF EXISTS healthcare_provider_oltp;"
        cursor.execute(drop_oltp_query)

        create_oltp_query = "CREATE DATABASE healthcare_provider_oltp;"
        cursor.execute(create_oltp_query)
        print(f"Database 'healthcare_provider_oltp' created successfully 💿")

    except ObjectInUse:
        raise ObjectInUse

    cursor.close()

def build_olap(postgres_conn):

    postgres_conn.autocommit = True
    cursor = postgres_conn.cursor()
    try:
        drop_olap_query = "DROP DATABASE IF EXISTS healthcare_provider_olap;"
        cursor.execute(drop_olap_query)

        create_olap_query = "CREATE DATABASE healthcare_provider_olap;"
        cursor.execute(create_olap_query)
        print(f"Database 'healthcare_provider_olap' created successfully 💿")

    except ObjectInUse:
        raise ObjectInUse
        
    cursor.close()