output "rds_endpoint" {
  description = "The RDS instance endpoint"
  value       = aws_db_instance.rds_instance.endpoint
}

output "rds_sg_id" {
  description = "The ID of the security group attached to the RDS instance"
  value       = aws_security_group.rds_sg.id
}
