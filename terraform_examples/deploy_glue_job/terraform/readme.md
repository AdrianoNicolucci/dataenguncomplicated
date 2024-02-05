### the following instructions are for deploying resources to AWS using terraform
1. terraform -chdir=terraform init --input=false
2. terraform -chdir=terraform plan --input=false --var-file=prod.tfvars
3.  