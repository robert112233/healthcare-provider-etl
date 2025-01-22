resource "aws_vpc" "healthcare_provider_etl" {
  cidr_block           = "10.0.0.0/24"
  enable_dns_hostnames = true

  tags = {
    Name = "healthcare-provider-etl"
  }
}

resource "aws_subnet" "healthcare_provider_rds_subnet" {
  count                   = 2
  vpc_id                  = aws_vpc.healthcare_provider_etl.id
  cidr_block              = var.subnet_ranges[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true
  # I'm aware this is bad practice. It is to remove the need for a bastion server, which would be challenging to automate in this project

  tags = {
    Name = "healthcare-provider-etl"
  }
}

resource "aws_subnet" "healthcare_provider_mwaa_subnet" {
  count                   = 2
  vpc_id                  = aws_vpc.healthcare_provider_etl.id
  cidr_block              = var.subnet_ranges[count.index + 2]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = false

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

resource "aws_route_table" "healthcare_provider_public_route_table" {
  vpc_id = aws_vpc.healthcare_provider_etl.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.healthcare_provider_gateway.id
  }
}

resource "aws_route_table_association" "healthcare_provider_rds_subnet_route" {
  count          = 2
  subnet_id      = aws_subnet.healthcare_provider_rds_subnet[count.index].id
  route_table_id = aws_route_table.healthcare_provider_public_route_table.id
}

resource "aws_db_subnet_group" "healthcare_provider_db_group" {
  subnet_ids = tolist([for subnet in aws_subnet.healthcare_provider_rds_subnet : subnet.id])
}

resource "aws_eip" "healthcare_provider_nat_ip" {
  domain = "vpc"
}

resource "aws_nat_gateway" "healthcare_provider_nat_gateway" {
  allocation_id = aws_eip.healthcare_provider_nat_ip.id
  subnet_id     = aws_subnet.healthcare_provider_mwaa_subnet[0].id

}

resource "aws_route" "private_subnet_route_1" {
  route_table_id         = aws_route_table.private_route_table.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.healthcare_provider_nat_gateway.id
}

resource "aws_route_table" "private_route_table" {
  vpc_id = aws_vpc.healthcare_provider_etl.id
}

resource "aws_route_table_association" "private_subnet_association" {
  count          = 2
  subnet_id      = aws_subnet.healthcare_provider_mwaa_subnet[count.index].id
  route_table_id = aws_route_table.private_route_table.id
}
