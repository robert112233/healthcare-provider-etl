variable "DB_USERNAME" {}
variable "DB_PASSWORD" {}

variable "database_names" {
  default = ["healthcare_provider_oltp", "healthcare_provider_olap"]
}
