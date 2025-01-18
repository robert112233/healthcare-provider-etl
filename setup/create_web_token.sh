#!/bin/bash

source ../.env

URL=https://$MWAA_ENDPOINT/aws_mwaa/aws-console-sso?login=true#
WEB_TOKEN=$(aws mwaa create-web-login-token --name healthcare_mwaa_environment --query WebToken --output text)
echo $URL$WEB_TOKEN
