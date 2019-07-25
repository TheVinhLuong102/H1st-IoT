# main bucket for storage
resource "aws_s3_bucket" "storage" {
  bucket = var.storage_bucket_name
  acl    = "private"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  logging {
    target_bucket = "aws-logs-${data.aws_caller_identity.default.account_id}-${data.aws_region.default.name}"
    target_prefix = var.storage_bucket_name
  }

  tags = {
    Project     = var.project_tag
    Environment = var.environment_tag
  }
}

