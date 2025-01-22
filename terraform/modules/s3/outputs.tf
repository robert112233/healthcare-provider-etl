output "airflow_healthcare_provider_bucket_arn" {
  value = aws_s3_bucket.airflow_healthcare_provider_bucket.arn
}

output "healthcare_bucket_ids" {
  value = aws_s3_bucket.healthcare_bucket[*].id
}

output "airflow_healthcare_bucket_id" {
  value = aws_s3_bucket.airflow_healthcare_provider_bucket.id
}

output "bucket_suffix" {
  value       = random_string.bucket_suffix.result
  description = "The unique suffix for s3 buckets"
}
