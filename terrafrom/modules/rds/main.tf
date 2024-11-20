data "aws_ssm_parameter" "db_username" {
  name = var.db_username_ssm
}

data "aws_ssm_parameter" "db_password" {
  name            = var.db_password_ssm
  with_decryption = true
}

resource "aws_security_group" "rds_sg" {
  name        = "${var.db_identifier}-sg"
  description = "Allow public access to RDS"

  ingress {
    from_port   = var.db_port
    to_port     = var.db_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Public access
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = var.tags
}


resource "aws_db_instance" "rds_instance" {
  allocated_storage    = var.db_allocated_storage
  engine               = var.db_engine
  engine_version       = var.db_engine_version
  instance_class       = var.db_instance_class
  db_name              = var.db_name  # Correct attribute
  username             = data.aws_ssm_parameter.db_username.value
  password             = data.aws_ssm_parameter.db_password.value
  publicly_accessible  = var.publicly_accessible
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  skip_final_snapshot  = true

  tags = var.tags
}
