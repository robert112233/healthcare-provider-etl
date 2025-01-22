resource "aws_mwaa_environment" "healthcare_mwaa_environment" {
  name                  = "healthcare_mwaa_environment"
  dag_s3_path           = "dags/"
  requirements_s3_path  = "requirements.txt"
  execution_role_arn    = var.healthcare_mwaa_role_arn
  environment_class     = "mw1.small"
  airflow_version       = "2.10.3"
  max_workers           = 1
  min_workers           = 1
  schedulers            = 2
  webserver_access_mode = "PUBLIC_ONLY"

  network_configuration {
    security_group_ids = [var.healthcare_provider_security_id]
    subnet_ids         = [var.healthcare_provider_mwaa_subnet_ids[0], var.healthcare_provider_mwaa_subnet_ids[1]]
  }
  logging_configuration {
    dag_processing_logs {
      enabled   = true
      log_level = "INFO"
    }

    scheduler_logs {
      enabled   = true
      log_level = "INFO"
    }

    task_logs {
      enabled   = true
      log_level = "INFO"
    }

    webserver_logs {
      enabled   = true
      log_level = "INFO"
    }

    worker_logs {
      enabled   = true
      log_level = "INFO"
    }
  }
  airflow_configuration_options = {
    "webserver.log_fetch_timeout_sec" = "10"
  }
  source_bucket_arn = var.healthcare_provider_bucket_arn
}

output "mwaa_endpoint" {
  value = aws_mwaa_environment.healthcare_mwaa_environment.webserver_url
}
