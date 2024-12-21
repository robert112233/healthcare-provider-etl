resource "aws_db_instance" "oltp_db" {
  allocated_storage   = 10
  db_name             = "oltp_db"
  engine              = "postgres"
  engine_version      = "14.10"
  instance_class      = "db.t3.micro"
  username            = var.db_username
  password            = var.db_password
  skip_final_snapshot = true
  identifier          = var.db_identifier
  publicly_accessible = true
}

data "http" "myip" {
  url = "https://ipv4.icanhazip.com"
}


resource "aws_security_group" "oltp_security" {
  name        = "oltp_security"
  description = "Security group for oltp database"
  vpc_id      = "vpc-07fc709135a920dd3"
}

resource "aws_vpc_security_group_ingress_rule" "http_ipv4" {
  security_group_id = aws_security_group.oltp_security.id
  cidr_ipv4         = "${chomp(data.http.myip.response_body)}/32"
  from_port         = 5432
  ip_protocol       = "TCP"
  to_port           = 5432
}


resource "aws_vpc_security_group_egress_rule" "outgoing_ipv4" {
  security_group_id = aws_security_group.oltp_security.id

  cidr_ipv4   = "${chomp(data.http.myip.response_body)}/32"
  ip_protocol = "-1"
}

