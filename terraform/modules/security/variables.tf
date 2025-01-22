variable "vpc_id" {
  type = string
}

variable "healthcare_bucket_ids" {
  type = list(string)
}

variable "airflow_healthcare_bucket_id" {
  type = string
}
