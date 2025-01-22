output "aws_db_subnet_group_name" {
  value = aws_db_subnet_group.healthcare_provider_db_group.name
}

output "vpc_id" {
  value = aws_vpc.healthcare_provider_etl.id
}

output "healthcare_provider_mwaa_subnet_ids" {
  value = aws_subnet.healthcare_provider_mwaa_subnet[*].id
}
