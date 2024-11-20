variable "db_identifier" {
  description = "Unique identifier for the RDS instance"
  type        = string
}

variable "db_engine" {
  description = "Database engine (e.g., PostgreSQL)"
  type        = string
  default     = "postgres"
}

variable "db_engine_version" {
  description = "Version of the database engine"
  type        = string
  default     = "13.16"
}

variable "db_instance_class" {
  description = "RDS instance type"
  type        = string
  default     = "db.t3.micro"  # Free-tier eligible
}

variable "db_name" {
  description = "Name of the database"
  type        = string
}

variable "db_allocated_storage" {
  description = "Allocated storage for the RDS instance (in GB)"
  type        = number
  default     = 20
}

variable "db_port" {
  description = "Port for the database"
  type        = number
  default     = 5432
}

variable "db_username_ssm" {
  description = "SSM Parameter name for the database username"
  type        = string
}

variable "db_password_ssm" {
  description = "SSM Parameter name for the database password"
  type        = string
}

variable "publicly_accessible" {
  description = "Make the RDS instance publicly accessible"
  type        = bool
  default     = true
}

variable "tags" {
  description = "Tags to apply to the RDS instance and security group"
  type        = map(string)
  default     = {}
}
