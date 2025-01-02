SHELL=/bin/bash
PYTHONPATH=$(shell pwd)
INSERTION_TERRAFORM_DIR = ./terraform/insertion

.PHONY: setup

apply_insertion: 
	@dotenv run terraform -chdir=$(INSERTION_TERRAFORM_DIR) apply -auto-approve

destroy_insertion: 
	@dotenv run terraform -chdir=$(INSERTION_TERRAFORM_DIR) destroy -auto-approve

setup:
	python ./setup/setup.py