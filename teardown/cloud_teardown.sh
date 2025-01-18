cd terraform

if [ -f .env ]; then
  export $(cat .env | xargs)
fi

terraform destroy -auto-approve 