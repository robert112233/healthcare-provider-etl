import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
import sys
from psycopg2.errors import ObjectInUse, DuplicateDatabase

def build_oltp(postgres_conn): 
    postgres_conn.autocommit = True
    cursor = postgres_conn.cursor()
    # cursor.execute(
    # """SELECT datname, usename, client_addr, state, COUNT(*) 
    #     FROM pg_stat_activity 
    #     GROUP BY datname, usename, client_addr, state;""")
    
    # result = cursor.fetchall()

    # for row in result:
    #     print(row, "a row, last value is the conn amount")

    try:
        # drop_oltp_query = "DROP DATABASE IF EXISTS healthcare_provider_oltp;"
        # cursor.execute(drop_oltp_query)
        create_oltp_query = "CREATE DATABASE healthcare_provider_oltp;"
        cursor.execute(create_oltp_query)
        print(f"Database 'healthcare_provider_oltp' created successfully 💿")

    except DuplicateDatabase:
        print("Database already exists! Skipping")

    cursor.close()

def build_olap(postgres_conn):

    postgres_conn.autocommit = True
    cursor = postgres_conn.cursor()
    try:
        # drop_olap_query = "DROP DATABASE IF EXISTS healthcare_provider_olap;"
        # cursor.execute(drop_olap_query)

        create_olap_query = "CREATE DATABASE healthcare_provider_olap;"
        cursor.execute(create_olap_query)
        print(f"Database 'healthcare_provider_olap' created successfully 💿\n")

    except DuplicateDatabase:
        print("Database already exists! Skipping")
        
    cursor.close()