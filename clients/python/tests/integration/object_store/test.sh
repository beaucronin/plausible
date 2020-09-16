#!/bin/bash

cd infra
echo Terraform INIT
terraform init > /dev/null
echo Terraform APPLY
terraform apply -no-color -auto-approve

echo ---------------------------
cd ..
echo Running tests
cp infra/terraform.tfstate .
python tests.py

echo ---------------------------
cd infra
echo TERRAFORM DESTROY
terraform destroy -no-color -auto-approve