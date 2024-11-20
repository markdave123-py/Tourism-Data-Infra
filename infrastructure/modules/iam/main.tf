resource "aws_iam_user" "user" {
  name = var.user_name
}

# S3 Policy
resource "aws_iam_policy" "s3_policy" {
  name        = "s3-access-policy"
  description = "Least privilege policy for S3 access"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid    = "AllowS3ObjectActions",
        Effect = "Allow",
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:HeadObject",
          "s3:DeleteObject",
          "s3:GetObjectAcl",
          "s3:PutObjectAcl"
        ],
        Resource = "arn:aws:s3:::cde-milestone-obs-travel-agency/*"
      },
      {
        Sid    = "AllowS3BucketActions",
        Effect = "Allow",
        Action = [
          "s3:ListBucket",
          "s3:GetBucketOwnershipControls"
        ],
        Resource = "arn:aws:s3:::cde-milestone-obs-travel-agency"
      }
    ]
  })
}

# SSM Policy
resource "aws_iam_policy" "ssm_policy" {
  name        = "ssm-access-policy"
  description = "Least privilege policy for SSM access"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters",
          "ssm:GetParameterHistory"
        ],
        Resource = [
          "arn:aws:ssm:eu-central-1:637423554954:parameter/rds-username-cde",
          "arn:aws:ssm:eu-central-1:637423554954:parameter/rds-password-cde"
        ]
      }
    ]
  })
}

# RDS Policy
resource "aws_iam_policy" "rds_policy" {
  name        = "rds-access-policy"
  description = "Least privilege policy for RDS access"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "rds:DescribeDBInstances",
          "rds:Connect"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_user_policy_attachment" "s3_policy_attachment" {
  user       = aws_iam_user.user.name
  policy_arn = aws_iam_policy.s3_policy.arn
}

resource "aws_iam_user_policy_attachment" "ssm_policy_attachment" {
  user       = aws_iam_user.user.name
  policy_arn = aws_iam_policy.ssm_policy.arn
}

resource "aws_iam_user_policy_attachment" "rds_policy_attachment" {
  user       = aws_iam_user.user.name
  policy_arn = aws_iam_policy.rds_policy.arn
}
