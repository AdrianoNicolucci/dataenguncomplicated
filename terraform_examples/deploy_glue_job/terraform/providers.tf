terraform {
  required_version = "~> 1.6.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.30.0"  # Replace with your desired version constraint
    }
    ## ..
    }
  }

  provider "aws" {
    region = "ca-central-1"  # Set your desired AWS region
    profile = "default"
}

terraform {
  backend "s3" {
    bucket = "adriano-data-uploads"
    key    = "terraform/terraform.tfstate"
    region = "ca-central-1"
    profile = "default"
  }
}