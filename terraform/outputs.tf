output "bucket_suffix" {
  value       = module.s3.bucket_suffix
  description = "The unique suffix for s3 buckets"
}

output "rds_endpoint" {
  value       = module.rds.rds_endpoint
  description = "The endpoint of the RDS instance"
}

output "mwaa_endpoint" {
  value = module.mwaa.mwaa_endpoint
}

output "S3_IAM_ACCESS_KEY_ID" {
  value     = module.security.s3_iam_access_key_id
  sensitive = true
}

output "S3_IAM_SECRET_ACCESS_KEY" {
  value     = module.security.s3_iam_secret_access_key
  sensitive = true
}
