SHELL=/bin/bash
PYTHONPATH=$(shell pwd)
INSERTION_TERRAFORM_DIR = ./terraform/insertion

.PHONY: setup teardown dashboard

setup:
	python ./setup/setup.py

teardown:
	python ./teardown/teardown.py

lint: 
	flake8 --exclude=venv

dashboard:
	streamlit run ./streamlit/app.py