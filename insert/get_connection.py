from get_db_details import get_db_details
import os
from pg8000.native import Connection
from dotenv import load_dotenv

def get_connection():
    try:
        load_dotenv()
        identifier = os.environ['TF_VAR_db_identifier']
        password = os.environ['TF_VAR_db_password']
        db_details = get_db_details(identifier)
        return Connection(
            'postgres', password = password, host = db_details['host'], port = db_details['port'], database = db_details['db_name']
        )
    except Exception as e:
        print(f'Something went wrong: {e}')

