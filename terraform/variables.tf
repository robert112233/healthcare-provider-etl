variable "DB_USERNAME" {}
variable "DB_PASSWORD" {}

data "aws_caller_identity" "account" {}
data "aws_region" "current" {}

variable "account_id" {
  default = data.aws_caller_identity.account.account_id
}

variable "region" {
  default = data.aws_region.region.name
}

variable "bucket_names" {
  default = ["healthcare-provider-etl-extract-bucket", "healthcare-provider-etl-transform-bucket"]
}

variable "subnet_ranges" {
  default = ["10.0.0.0/26", "10.0.0.64/26", "10.0.0.128/26", "10.0.0.192/26"]
}

variable "availability_zones" {
  default = ["eu-west-2a", "eu-west-2b"]
}

variable "database_names" {
  default = ["healthcare_provider_oltp", "healthcare_provider_olap"]
}
