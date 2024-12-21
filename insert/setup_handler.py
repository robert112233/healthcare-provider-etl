# from seed_patients import seed_patients
# from seed_appointments import seed_appointments
import logging
logger = logging.getLogger(__name__)

def setup_handler(event, context):
    logger.info("Handler invoked")
    return {"statusCode": 200, "body": "Success"}

# def setup_handler(event, context):
#     logger.setLevel('INFO')
#     logger.info("running setup_handler")
#     seed_patients()
#     seed_appointments()
#     return { 'statusCode': 200, 
#              'body': 'Lambda function executed successfully'
#            }