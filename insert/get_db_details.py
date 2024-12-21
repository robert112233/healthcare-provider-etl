import boto3

def get_db_details(db_identifier):
    rds_client = boto3.client('rds', region_name='eu-west-2')

    try:
        response = rds_client.describe_db_instances(DBInstanceIdentifier=db_identifier)
        address = response['DBInstances'][0]['Endpoint']['Address']
        port = response['DBInstances'][0]['Endpoint']['Port']
        db_name = response['DBInstances'][0]['DBName']
        return {'host': address, 'port': port, 'db_name': db_name}

    except Exception as e:
        print(f'Something went wrong: {e}')

get_db_details("oltp-db")