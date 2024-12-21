FROM public.ecr.aws/lambda/python:3.9

ENV AWS_REGION=eu-west-2
ENV AWS_LAMBDA_HANDLER=setup_handler.setup_handler

# COPY get_db_details.py /var/task/
# COPY get_connection.py /var/task/
# COPY create_random_patients.py /var/task/
# COPY seed_patients.py /var/task/
# COPY create_random_appointment.py /var/task/
# COPY seed_appointments.py /var/task/
# COPY insert_random_appointment.py /var/task/
# COPY update_random_appointment.py /var/task/
COPY setup_handler.py /var/task/

# RUN pip install pg8000 boto3 python-dotenv --target /var/task/
RUN pip install boto3 --target /var/task

CMD ["setup_handler.setup_handler"]