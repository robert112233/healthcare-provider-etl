data "aws_caller_identity" "account" {}
data "aws_region" "region" {}

resource "random_string" "bucket_suffix" {
  length  = 6
  special = false
  upper   = false
}

output "bucket_suffix" {
  value       = random_string.bucket_suffix.result
  description = "The unique suffix for s3 buckets"
}

resource "aws_s3_bucket" "healthcare_bucket" {
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

resource "aws_db_instance" "db" {
  db_subnet_group_name = aws_db_subnet_group.healthcare_provider_db_group.name
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
  vpc_security_group_ids = [aws_security_group.healthcare_provider_security.id]
}

output "rds_endpoint" {
  value       = aws_db_instance.db.endpoint
  description = "The endpoint of the RDS instance"
  depends_on  = [aws_db_instance.db]
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
  cidr_ipv4         = "5.151.29.0/24"
  from_port         = 5432
  to_port           = 5432
  ip_protocol       = "TCP"
}

resource "aws_vpc_security_group_ingress_rule" "https" {
  security_group_id = aws_security_group.healthcare_provider_security.id
  from_port         = 443
  to_port           = 443
  ip_protocol       = "TCP"
  cidr_ipv4         = "5.151.29.0/24"
}

resource "aws_vpc_security_group_egress_rule" "outbound_internet" {
  security_group_id = aws_security_group.healthcare_provider_security.id
  from_port         = 0
  to_port           = 0
  ip_protocol       = "TCP"
  cidr_ipv4         = "0.0.0.0/0"
}

resource "aws_iam_user" "healthcare_s3_user" {
  name = "healthcare_s3_user"

  tags = {
    tag-key = "healthcare-provider-etl"
  }
}

resource "aws_iam_access_key" "healthcare_s3_key" {
  user = aws_iam_user.healthcare_s3_user.name
}

data "aws_iam_policy_document" "healthcare_s3_policy" {
  statement {
    effect    = "Allow"
    actions   = ["s3:*"]
    resources = ["*"]
  }
}

resource "aws_iam_user_policy" "healthcare_s3_user_policy" {
  name   = "test"
  user   = aws_iam_user.healthcare_s3_user.name
  policy = data.aws_iam_policy_document.healthcare_s3_policy.json
}

output "s3_iam_access_key_id" {
  value       = aws_iam_access_key.healthcare_s3_key.id
  description = "The access key for s3 iam user"
  sensitive   = true
}

output "s3_iam_secret_access_key" {
  value       = aws_iam_access_key.healthcare_s3_key.secret
  description = "The access key for s3 iam user"
  sensitive   = true
}

resource "aws_s3_bucket" "airflow_healthcare_provider_bucket" {
  bucket = "airflow-healthcare-provider-etl-bucket-${random_string.bucket_suffix.result}"
  tags = {
    Name = "healthcare-provider-etl"
  }
}

resource "aws_s3_bucket_versioning" "versioning_example" {
  bucket = aws_s3_bucket.airflow_healthcare_provider_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_object" "etl_dag" {
  bucket       = aws_s3_bucket.airflow_healthcare_provider_bucket.id
  key          = "dags/etl.py"
  source       = "../DAGs/etl.py"
  content_type = "text/x-python"
}

resource "aws_s3_object" "update_appointments_dag" {
  bucket       = aws_s3_bucket.airflow_healthcare_provider_bucket.id
  key          = "dags/update_appointments.py"
  source       = "../DAGs/update_appointments.py"
  content_type = "text/x-python"
}

resource "aws_s3_object" "etl_utils" {
  bucket       = aws_s3_bucket.airflow_healthcare_provider_bucket.id
  key          = "dags/utils/etl_utils.py"
  source       = "../DAGs/utils/etl_utils.py"
  content_type = "text/x-python"
}

resource "aws_s3_object" "create_and_insert_utils" {
  bucket       = aws_s3_bucket.airflow_healthcare_provider_bucket.id
  key          = "dags/utils/create_and_insert_utils.py"
  source       = "../DAGs/utils/create_and_insert_utils.py"
  content_type = "text/x-python"
}

resource "aws_s3_object" "requirements" {
  bucket       = aws_s3_bucket.airflow_healthcare_provider_bucket.id
  key          = "requirements.txt"
  source       = "../DAGs/requirements.txt"
  content_type = "text/plain"
}

resource "aws_iam_role" "healthcare_mwaa_role" {
  name = "healthcare_mwaa_role"
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "airflow-env.amazonaws.com"
        },
        "Action" : "sts:AssumeRole"
      }
    ]
  })
}
resource "aws_iam_role_policy" "healthcare_mwaa_role_policy" {
  role = aws_iam_role.healthcare_mwaa_role.id
  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Sid" : "AllowMwaaRestApiAccess",
        "Effect" : "Allow",
        "Action" : "airflow:InvokeRestApi",
        "Resource" : [
          "arn:aws:airflow:${data.aws_region.region.name}:${data.aws_caller_identity.account.account_id}:role/airflow-healthcare_mwaa_environment/healthcare_mwaa_role"
        ]
      },
      {
        "Effect" : "Deny",
        "Action" : "s3:ListAllMyBuckets",
        "Resource" : [
          "arn:aws:s3:::${aws_s3_bucket.airflow_healthcare_provider_bucket.id}",
          "arn:aws:s3:::${aws_s3_bucket.airflow_healthcare_provider_bucket.id}/*",
          "arn:aws:s3:::${aws_s3_bucket.healthcare_bucket[0].id}/*",
          "arn:aws:s3:::${aws_s3_bucket.healthcare_bucket[0].id}",
          "arn:aws:s3:::${aws_s3_bucket.healthcare_bucket[1].id}/*",
          "arn:aws:s3:::${aws_s3_bucket.healthcare_bucket[1].id}"
        ]
      },
      {
        "Effect" : "Allow",
        "Action" : [
          "s3:GetObject*",
          "s3:GetBucket*",
          "s3:List*"
        ],
        "Resource" : [
          "arn:aws:s3:::${aws_s3_bucket.airflow_healthcare_provider_bucket.id}",
          "arn:aws:s3:::${aws_s3_bucket.airflow_healthcare_provider_bucket.id}/*",
          "arn:aws:s3:::${aws_s3_bucket.healthcare_bucket[0].id}/*",
          "arn:aws:s3:::${aws_s3_bucket.healthcare_bucket[0].id}",
          "arn:aws:s3:::${aws_s3_bucket.healthcare_bucket[1].id}/*",
          "arn:aws:s3:::${aws_s3_bucket.healthcare_bucket[1].id}"
        ]
      },
      {
        "Effect" : "Allow",
        "Action" : [
          "logs:CreateLogStream",
          "logs:CreateLogGroup",
          "logs:PutLogEvents",
          "logs:GetLogEvents",
          "logs:GetLogRecord",
          "logs:GetLogGroupFields",
          "logs:GetQueryResults"
        ],
        "Resource" : [
          "arn:aws:logs:${data.aws_region.region.name}:${data.aws_caller_identity.account.account_id}:log-group:airflow-healthcare_mwaa_environment-*"
        ]
      },
      {
        "Effect" : "Allow",
        "Action" : [
          "logs:DescribeLogGroups"
        ],
        "Resource" : [
          "arn:aws:logs:${data.aws_region.region.name}:${data.aws_caller_identity.account.account_id}:log-group:airflow-healthcare_mwaa_environment-*"
        ]
      },
      {
        "Effect" : "Allow",
        "Action" : [
          "s3:GetAccountPublicAccessBlock"
        ],
        "Resource" : [
          "arn:aws:s3:::${aws_s3_bucket.airflow_healthcare_provider_bucket.id}",
          "arn:aws:s3:::${aws_s3_bucket.airflow_healthcare_provider_bucket.id}/*",
          "arn:aws:s3:::${aws_s3_bucket.healthcare_bucket[0].id}/*",
          "arn:aws:s3:::${aws_s3_bucket.healthcare_bucket[0].id}",
          "arn:aws:s3:::${aws_s3_bucket.healthcare_bucket[1].id}/*",
          "arn:aws:s3:::${aws_s3_bucket.healthcare_bucket[1].id}"
        ]
      },
      {
        "Effect" : "Allow",
        "Action" : "cloudwatch:PutMetricData",
        "Resource" : ["*"]
      },
      {
        "Effect" : "Allow",
        "Action" : [
          "sqs:ChangeMessageVisibility",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes",
          "sqs:GetQueueUrl",
          "sqs:ReceiveMessage",
          "sqs:SendMessage"
        ],
        "Resource" : "arn:aws:sqs:${data.aws_region.region.name}:*:airflow-celery-*"
      },
    ]
  })
}

resource "aws_mwaa_environment" "healthcare_mwaa_environment" {
  name                  = "healthcare_mwaa_environment"
  dag_s3_path           = "dags/"
  requirements_s3_path  = "requirements.txt"
  execution_role_arn    = aws_iam_role.healthcare_mwaa_role.arn
  environment_class     = "mw1.small"
  airflow_version       = "2.10.3"
  max_workers           = 1
  min_workers           = 1
  schedulers            = 2
  webserver_access_mode = "PUBLIC_ONLY"

  network_configuration {
    security_group_ids = [aws_security_group.healthcare_provider_security.id]
    subnet_ids         = [aws_subnet.healthcare_provider_mwaa_subnet[0].id, aws_subnet.healthcare_provider_mwaa_subnet[1].id]
  }
  airflow_configuration_options = {
    "webserver.log_fetch_timeout_sec" = "10"
  }
  source_bucket_arn = aws_s3_bucket.airflow_healthcare_provider_bucket.arn
}

output "mwaa_endpoint" {
  value = aws_mwaa_environment.healthcare_mwaa_environment.webserver_url
}
