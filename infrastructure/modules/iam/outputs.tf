output "user_name" {
  description = "The name of the IAM user"
  value       = aws_iam_user.user.name
}
