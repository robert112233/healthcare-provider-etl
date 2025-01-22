module "mwaa" {
  source                              = "./modules/mwaa"
  healthcare_provider_bucket_arn      = module.s3.airflow_healthcare_provider_bucket_arn
  healthcare_mwaa_role_arn            = module.security.healthcare_mwaa_role_arn
  healthcare_provider_security_id     = module.security.health_care_provider_security_id
  healthcare_provider_mwaa_subnet_ids = module.vpc.healthcare_provider_mwaa_subnet_ids

}

module "rds" {
  source                           = "./modules/rds"
  DB_USERNAME                      = var.DB_USERNAME
  DB_PASSWORD                      = var.DB_PASSWORD
  db_subnet_group_name             = module.vpc.aws_db_subnet_group_name
  health_care_provider_security_id = module.security.health_care_provider_security_id
}

module "s3" {
  source = "./modules/s3"
}

module "security" {
  source                       = "./modules/security"
  vpc_id                       = module.vpc.vpc_id
  healthcare_bucket_ids        = module.s3.healthcare_bucket_ids
  airflow_healthcare_bucket_id = module.s3.airflow_healthcare_bucket_id
}

module "vpc" {
  source = "./modules/vpc"
}

