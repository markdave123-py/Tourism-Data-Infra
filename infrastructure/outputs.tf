output "iam_user_name" {
  description = "The IAM user name"
  value       = module.iam.user_name
}

output "s3_bucket_name" {
  description = "The name of the S3 bucket"
  value       = module.s3.bucket_name
}

output "rds_endpoint" {
  description = "The RDS endpoint"
  value       = module.rds.rds_endpoint
}