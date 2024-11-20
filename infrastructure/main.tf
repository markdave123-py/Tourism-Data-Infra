provider "aws" {
  region = var.aws_region
}

# IAM Module
module "iam" {
  source      = "./modules/iam"
  user_name   = var.project_user_name
}

# S3 Module
module "s3" {
  source           = "./modules/s3"
  bucket_name      = var.s3_bucket_name
  enable_versioning = true
}

# RDS Module
module "rds" {
  source              = "./modules/rds"
  db_identifier       = var.rds_identifier
  db_engine           = "postgres"
  db_engine_version   = "13.16"
  db_instance_class   = "db.t3.micro"
  db_name             = var.rds_db_name
  db_allocated_storage = var.rds_allocated_storage
  db_port             = 5432
  db_username_ssm     = "rds-username-cde"
  db_password_ssm     = "rds-password-cde"
  publicly_accessible = true
  tags = {
    Environment = "dev"
    Project     = "milestone"
  }
}




terraform {
  backend "s3" {
    bucket         = "my-terraform-state-bucket-cde-milestone-travel-agency"
    key            = "terraform/state/terraform.tfstate"
    region         = "eu-central-1"
    encrypt        = true
  }
}

# resource "aws_s3_bucket" "tf_state" {
#   bucket = var.tf_state_bucket_name

#   tags = {
#     Name        = "TerraformStateBucket"
#     Environment = "Dev"
#   }
# }

# resource "aws_s3_bucket_versioning" "tf_state_versioning" {
#   bucket = aws_s3_bucket.tf_state.id

#   versioning_configuration {
#     status = "Enabled"
#   }
# }
