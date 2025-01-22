data "http" "myip" {
  url = "https://ipv4.icanhazip.com"
}

data "aws_caller_identity" "account" {}

data "aws_region" "region" {}


resource "aws_security_group" "healthcare_provider_security" {
  name        = "healthcare_provider_security"
  description = "Security group for database"
  vpc_id      = var.vpc_id
}

resource "aws_vpc_security_group_ingress_rule" "temp_postgres_acess" {
  security_group_id = aws_security_group.healthcare_provider_security.id
  cidr_ipv4         = "${chomp(data.http.myip.response_body)}/32"
  from_port         = 5432
  to_port           = 5432
  ip_protocol       = "TCP"
}

resource "aws_vpc_security_group_ingress_rule" "https" {
  security_group_id = aws_security_group.healthcare_provider_security.id
  from_port         = 443
  to_port           = 443
  ip_protocol       = "TCP"
  cidr_ipv4         = "${chomp(data.http.myip.response_body)}/32"
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
          "arn:aws:s3:::${var.airflow_healthcare_bucket_id}",
          "arn:aws:s3:::${var.airflow_healthcare_bucket_id}/*",
          "arn:aws:s3:::${var.healthcare_bucket_ids[0]}/*",
          "arn:aws:s3:::${var.healthcare_bucket_ids[0]}",
          "arn:aws:s3:::${var.healthcare_bucket_ids[1]}/*",
          "arn:aws:s3:::${var.healthcare_bucket_ids[1]}"
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
          "arn:aws:s3:::${var.airflow_healthcare_bucket_id}",
          "arn:aws:s3:::${var.airflow_healthcare_bucket_id}/*",
          "arn:aws:s3:::${var.healthcare_bucket_ids[0]}/*",
          "arn:aws:s3:::${var.healthcare_bucket_ids[0]}",
          "arn:aws:s3:::${var.healthcare_bucket_ids[1]}/*",
          "arn:aws:s3:::${var.healthcare_bucket_ids[1]}"
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
          "arn:aws:s3:::${var.airflow_healthcare_bucket_id}",
          "arn:aws:s3:::${var.airflow_healthcare_bucket_id}/*",
          "arn:aws:s3:::${var.healthcare_bucket_ids[0]}/*",
          "arn:aws:s3:::${var.healthcare_bucket_ids[0]}",
          "arn:aws:s3:::${var.healthcare_bucket_ids[1]}/*",
          "arn:aws:s3:::${var.healthcare_bucket_ids[1]}"
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
