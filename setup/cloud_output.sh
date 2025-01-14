cd terraform

RDS_ENDPOINT=$(terraform output -raw rds_endpoint)
BUCKET_SUFFIX=$(terraform output -raw bucket_suffix)
S3_IAM_ACCESS_KEY_ID=$(terraform output -raw s3_iam_access_key_id)
S3_IAM_SECRET_ACCESS_KEY=$(terraform output -raw s3_iam_secret_access_key)
MWAA_ENDPOINT=$(terraform output -raw mwaa_endpoint)

echo "$RDS_ENDPOINT" 
echo "$BUCKET_SUFFIX"
echo "$S3_IAM_ACCESS_KEY_ID"
echo "$S3_IAM_SECRET_ACCESS_KEY"
echo "$MWAA_ENDPOINT"