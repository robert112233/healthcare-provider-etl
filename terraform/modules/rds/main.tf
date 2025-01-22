resource "aws_db_instance" "db" {
  db_subnet_group_name = var.db_subnet_group_name
  allocated_storage    = 10
  db_name              = "postgres"
  engine               = "postgres"
  engine_version       = "14.15"
  instance_class       = "db.t3.micro"
  username             = var.DB_USERNAME
  password             = var.DB_PASSWORD
  skip_final_snapshot  = true
  identifier           = "oltp-olap"
  publicly_accessible  = true
  # I'm aware this is bad practice. It is to remove the need for a bastion server, which would be challenging to automate.
  vpc_security_group_ids = [var.health_care_provider_security_id]
}

