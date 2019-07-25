resource "aws_instance" "app" {
  ami                    = "ami-08f57bb51048be421"
  instance_type          = "m5.xlarge"
  subnet_id              = var.subnet1_id
  vpc_security_group_ids = [var.internal_security_group_id]
  user_data              = module.ssh.user_data

  root_block_device {
    volume_type = "gp2"
    volume_size = "128"
  }

  tags = {
    Name        = "CCPM - App"
    Cluster     = "CCPM"
    Vendor      = "ARIMO"
    Environment = var.environment_tag
    Project     = var.project_tag
  }

  lifecycle {
    ignore_changes = [
      ami,
      user_data,
    ]
  }
}

resource "aws_db_instance" "app-db" {
  allocated_storage       = 864
  backup_retention_period = 3
  db_subnet_group_name    = "pm20190118201546865800000001"
  engine                  = "postgres"
  engine_version          = "10.6"
  identifier              = "ccpm-app-db"
  instance_class          = "db.m4.large"
  multi_az                = false
  name                    = "ccpm"

  snapshot_identifier = "ccpm-app-db-20190624"

  # XXX FIX: This means the password is in state file.
  # password               = "${trimspace(file("${path.module}/secrets/app-db-password"))}"
  port = 5432

  publicly_accessible    = false
  storage_encrypted      = true
  storage_type           = "gp2"
  username               = "ccpm"
  vpc_security_group_ids = [var.internal_security_group_id]

  # monitoring_interval = 60

  tags = {
    Name        = "PM App DB"
    Project     = "CCPM"
    Environment = "DEV"
  }
}

resource "aws_db_instance" "fcpm-app-db" {
  allocated_storage       = 864
  backup_retention_period = 3
  db_subnet_group_name    = "pm20190118201546865800000001"
  engine                  = "postgres"
  engine_version          = "10.6"
  identifier              = "fcpm-app-db"
  instance_class          = "db.m4.large"
  multi_az                = false
  name                    = "fcpm"

  snapshot_identifier = "rds:ccpm-app-db-2019-07-22-10-30"

  # XXX FIX: This means the password is in state file.
  # password               = "${trimspace(file("${path.module}/secrets/app-db-password"))}"
  port = 5432

  publicly_accessible    = false
  storage_encrypted      = true
  storage_type           = "gp2"
  username               = "fcpm"
  vpc_security_group_ids = [var.internal_security_group_id]

  # monitoring_interval = 60

  tags = {
    Name        = "FC App DB"
    Project     = "FCPM"
    Environment = "DEV"
  }
}

module "app_ingress_jp" {
  source = "./ingress"
  name   = "ccpm-app-jp"

  load_balancer_name = "infra"
  zone_id            = data.aws_route53_zone.external.id
  domain_prefix      = "pm-app.jp"
  instances          = [aws_instance.app.id]
  instance_count     = 1
}

