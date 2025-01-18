**Healthcare Provider ETL**

This a project designed to showcase an etl pipeline using Apache Airflow, Terraform and Managed Workflows for Apache Airflow (MWAA)

A large amount of data is randomly created with custom functions then inserted. Subsequent data inserts & updates happen via a scheduled DAG. This runs independently from the ETL dag which ingests, formats and loads data into the olap database every 20 minutes.

You have the option to provision airflow locally or via the cloud. If you choose the latter, terraform will provision s3 buckets, RDS instances and a MWAA environment to your account. This can take around 20 minutes to build, so be patient. If you choose to run the project locally, be aware it will write data to your /tmp directory, which will be removed automatically by your operating system.

This project is intended to be easy to run for those who don't have immeadiate access to an AWS account, hence the use of credentials in .env instead of using secrets manager. The project also focuses on automation and is not suitable for production.

Prerequisites:

- [Postgresql installation](https://www.postgresql.org/download/)
- [Terraform installation](https://developer.hashicorp.com/terraform/install)
- [AWS IAM user with credentials in ~/.aws/credentials file](https://docs.aws.amazon.com/streams/latest/dev/setting-up.html)

To run this project:

ANYTHING YOU ADD TO THIS WILL AFFECT THE ERROR HANDLING IN SETUP.PY. DELETE ME AFTER.

1. Create and activate the virtual environment.

2. Run `pip install -r requirements.txt`

3. Fill out the initial environment variables in a `.env` file (See `.env.example` for the template)

4. Run this command to tell airflow where to look `export AIRFLOW__CORE__DAGS_FOLDER=$(pwd)/DAGs`

5. If you've never used airflow before, you will need to create an admin user with these credentials:

   ````
   airflow users create \
   --username admin \
   --firstname Admin \
   --lastname User \
   --role Admin \
   --email admin@admin.com \
   --password admin```
   ````

6. If running locally, start the webserver with `airflow webserver --port 8081` and start the scheduler with `airflow scheduler`.

7. Run `make setup` and follow the prompts.

8. You can view the webserver on `localhost:8081` if running locally, or find the MWAA endpoint if running via the cloud. Due to the way airflows schedule intervals work you may have to wait 20 minutes before seeing data. A DAG scheduled for 8:00 will _run_ at 8:20, as that's when the scheduled interval finishes.

9. Upon finishing, run `make teardown` to destroy the databases, connections, and any cloud infrastructure.
