variable "healthcare_provider_bucket_arn" {
  type = string
}

variable "healthcare_mwaa_role_arn" {
  type = string
}

variable "healthcare_provider_security_id" {
  type = string
}

variable "healthcare_provider_mwaa_subnet_ids" {
  type = list(string)
}
