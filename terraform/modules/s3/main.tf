resource "random_string" "bucket_suffix" {
  length  = 6
  special = false
  upper   = false
}

resource "aws_s3_bucket" "healthcare_bucket" {
  bucket = "${var.bucket_names[count.index]}-${random_string.bucket_suffix.result}"
  count  = 2


  tags = {
    Name = "healthcare-provider-etl"
  }
}

resource "aws_s3_bucket" "airflow_healthcare_provider_bucket" {
  bucket = "airflow-healthcare-provider-etl-bucket-${random_string.bucket_suffix.result}"
  tags = {
    Name = "healthcare-provider-etl"
  }
}

resource "aws_s3_bucket_versioning" "versioning_example" {
  bucket = aws_s3_bucket.airflow_healthcare_provider_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_object" "etl_dag" {
  bucket       = aws_s3_bucket.airflow_healthcare_provider_bucket.id
  key          = "dags/etl.py"
  source       = "../DAGs/etl.py"
  content_type = "text/x-python"
}

resource "aws_s3_object" "update_appointments_dag" {
  bucket       = aws_s3_bucket.airflow_healthcare_provider_bucket.id
  key          = "dags/update_appointments.py"
  source       = "../DAGs/update_appointments.py"
  content_type = "text/x-python"
}

resource "aws_s3_object" "etl_utils" {
  bucket       = aws_s3_bucket.airflow_healthcare_provider_bucket.id
  key          = "dags/utils/etl_utils.py"
  source       = "../DAGs/utils/etl_utils.py"
  content_type = "text/x-python"
}

resource "aws_s3_object" "create_and_insert_utils" {
  bucket       = aws_s3_bucket.airflow_healthcare_provider_bucket.id
  key          = "dags/utils/create_and_insert_utils.py"
  source       = "../DAGs/utils/create_and_insert_utils.py"
  content_type = "text/x-python"
}

resource "aws_s3_object" "requirements" {
  bucket       = aws_s3_bucket.airflow_healthcare_provider_bucket.id
  key          = "requirements.txt"
  source       = "../DAGs/requirements.txt"
  content_type = "text/plain"
}
