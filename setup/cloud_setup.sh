#!/bin/bash

if [ -f .env ]; then
  export $(cat .env | xargs)
fi

cd terraform

terraform init

terraform apply -auto-approve 