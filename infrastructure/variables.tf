variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "eu-central-1"
}

variable "project_user_name" {
  description = "IAM user name"
  type        = string
}

variable "s3_bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "rds_identifier" {
  description = "Unique identifier for the RDS instance"
  type        = string
}

variable "rds_db_name" {
  description = "Name of the database"
  type        = string
}

variable "rds_allocated_storage" {
  description = "Allocated storage for the RDS instance"
  type        = number
  default     = 20
}

variable "tf_state_bucket_name" {
  description = "Name of the S3 bucket for Terraform state"
  type        = string
}
