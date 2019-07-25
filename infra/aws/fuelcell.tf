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

resource "aws_instance" "fc-app" {
  ami                    = "ami-0aa089a4b0f0b97e9"  # ccpm-app-20190725
  instance_type          = "m5.xlarge"
  subnet_id              = var.subnet1_id
  vpc_security_group_ids = [var.internal_security_group_id]
  user_data              = module.ssh.user_data

  root_block_device {
    volume_type = "gp2"
    volume_size = "128"
  }

  tags = {
    Name        = "FCPM - App"
    Cluster     = "FCPM"
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

module "fc-app-ingress" {
  source = "./ingress"
  name   = "fcpm-app-jp"

  load_balancer_name = "infra"
  zone_id            = data.aws_route53_zone.external.id
  domain_prefix      = "fc-app"
  instances          = [aws_instance.fc-app.id]
  instance_count     = 1
}
