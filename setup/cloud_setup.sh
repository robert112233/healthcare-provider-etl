#!/bin/bash

if [ -f .env ]; then
  export $(cat .env | xargs)
fi

cd terraform

terraform init

terraform apply -auto-approve

RDS_ENDPOINT=$(terraform output -raw rds_endpoint)

echo "$RDS_ENDPOINT"