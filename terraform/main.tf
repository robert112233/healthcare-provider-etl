resource "random_string" "bucket_suffix" {
  length  = 6
  special = false
  upper   = false
}

resource "aws_s3_bucket" "example" {
  bucket = "${var.bucket_names[count.index]}-${random_string.bucket_suffix.result}"
  count  = 2


  tags = {
    Name = "healthcare-provider-etl"
  }
}

resource "aws_vpc" "healthcare_provider_etl" {
  cidr_block           = "10.0.0.0/24"
  enable_dns_hostnames = true

  tags = {
    Name = "healthcare-provider-etl"
  }
}

resource "aws_subnet" "healthcare_provider_subnet" {
  count                   = 2
  vpc_id                  = aws_vpc.healthcare_provider_etl.id
  cidr_block              = var.subnet_ranges[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name = "healthcare-provider-etl"
  }
}

resource "aws_internet_gateway" "healthcare_provider_gateway" {
  vpc_id = aws_vpc.healthcare_provider_etl.id

  tags = {
    Name = "healthcare-provider-etl"
  }
}

resource "aws_route_table" "healthcare_provider_route_table" {
  vpc_id = aws_vpc.healthcare_provider_etl.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.healthcare_provider_gateway.id
  }
}

resource "aws_route_table_association" "healthcare_provider_subnet_route" {
  count          = 2
  subnet_id      = aws_subnet.healthcare_provider_subnet[count.index].id
  route_table_id = aws_route_table.healthcare_provider_route_table.id
}

resource "aws_db_subnet_group" "healthcare_provider_db_group" {
  subnet_ids = tolist([for subnet in aws_subnet.healthcare_provider_subnet : subnet.id])
}

resource "aws_db_instance" "db" {
  db_subnet_group_name   = aws_db_subnet_group.healthcare_provider_db_group.name
  allocated_storage      = 10
  db_name                = "postgres"
  engine                 = "postgres"
  engine_version         = "14.10"
  instance_class         = "db.t3.micro"
  username               = var.DB_USERNAME
  password               = var.DB_PASSWORD
  skip_final_snapshot    = true
  identifier             = "oltp-olap"
  publicly_accessible    = true
  vpc_security_group_ids = [aws_security_group.healthcare_provider_security.id]
}

output "rds_endpoint" {
  value       = aws_db_instance.db.endpoint
  description = "The endpoint of the RDS instance"
}

data "http" "myip" {
  url = "https://ipv4.icanhazip.com"
}


resource "aws_security_group" "healthcare_provider_security" {
  name        = "healthcare_provider_security"
  description = "Security group for database"
  vpc_id      = aws_vpc.healthcare_provider_etl.id
}

resource "aws_vpc_security_group_ingress_rule" "temp_postgres_acess" {
  security_group_id = aws_security_group.healthcare_provider_security.id
  cidr_ipv4         = "${chomp(data.http.myip.response_body)}/32"
  from_port         = 5432
  ip_protocol       = "TCP"
  to_port           = 5432
}
