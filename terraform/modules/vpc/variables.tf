variable "subnet_ranges" {
  default = ["10.0.0.0/26", "10.0.0.64/26", "10.0.0.128/26", "10.0.0.192/26"]
}

variable "availability_zones" {
  default = ["eu-west-2a", "eu-west-2b"]
}
