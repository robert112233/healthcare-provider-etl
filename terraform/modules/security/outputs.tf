output "healthcare_mwaa_role_arn" {
  value = aws_iam_role.healthcare_mwaa_role.arn
}


output "health_care_provider_security_id" {
  value = aws_security_group.healthcare_provider_security.id
}

output "s3_iam_access_key_id" {
  value       = aws_iam_access_key.healthcare_s3_key.id
  description = "The access key for s3 iam user"
  sensitive   = true
}

output "s3_iam_secret_access_key" {
  value       = aws_iam_access_key.healthcare_s3_key.secret
  description = "The access key for s3 iam user"
  sensitive   = true
}
