#!/bin/bash

cd infra
terraform init
terraform apply

cd ..
cp infra/terraform.tfstate .
python -m tests.py

cd infra
terraform destroy