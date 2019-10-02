data "aws_iam_policy_document" "fc_s3_access" {
  statement {
    actions = ["s3:*"]
    resources = [
      "arn:aws:s3:::arimo-bai/*",
      "arn:aws:s3:::arimo-iot-pm/*",
      # "arn:aws:s3:::arimo-panasonic-ap",
      # "arn:aws:s3:::arimo-panasonic-ap/*",
      "arn:aws:s3:::arimo-panasonic-ap-jp-cc-pm",
      "arn:aws:s3:::arimo-panasonic-ap-jp-cc-pm/*",
      "arn:aws:s3:::arimo-panasonic-ap-jp-fc-pm",
      "arn:aws:s3:::arimo-panasonic-ap-jp-fc-pm/*",
      "arn:aws:s3:::arimo-panasonic-iot-pm",
      "arn:aws:s3:::arimo-panasonic-iot-pm/*",
      "arn:aws:s3:::arimo-bai-clusters/custom_provisioner/ccpm*",
    ]
  }

  statement {
    actions = [
      "s3:GetBucketLocation",
      "s3:ListAllMyBuckets",
    ]

    resources = ["arn:aws:s3:::*"]
  }
}

resource "aws_iam_role" "fc_role" {
  name               = "fcpm-yarn"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json
}

resource "aws_iam_instance_profile" "fc_role" {
  name = aws_iam_role.fc_role.name
  role = aws_iam_role.fc_role.name
}

resource "aws_iam_role_policy" "fc_node_s3_policy" {
  name   = "fc-s3-access"
  policy = data.aws_iam_policy_document.fc_s3_access.json
  role   = aws_iam_role.fc_role.id
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

module "fc-jupyter" {
  source = "./gpu-jupyter"

  name               = "fcpm-jupyter"
  subnet_id          = var.subnet1_id
  security_group_ids = [var.internal_security_group_id]
  instance_profile   = aws_iam_instance_profile.fc_role.name
  ssh_user_data      = module.ssh.user_data

  project_tag = "FCPM"

  instance_type = "g3.16xlarge"

  domain = "fcpm-jupyter.jp"
}

module "fc-yarn-xlarge" {
  source             = "./yarn-cluster"
  name               = "fcpm-xlarge"
  domain             = "yarn-fcpm-xlarge.jp"
  subnet_id          = var.subnet1_id
  security_group_ids = [var.internal_security_group_id]
  instance_profile   = aws_iam_instance_profile.fc_role.name

  installer_version  = "1.3.2"

  ssh_user_data    = module.ssh.user_data
  s3_config_bucket = var.storage_bucket_name

  # TODO : support ebs for master node

  workers              = 3
  instance_type        = "c5n.18xlarge"
  master_instance_type = "m5a.2xlarge"
  yarn_worker_memory   = "192000"
  project_tag          = "FCPM"
  environment_tag      = var.environment_tag

  cluster_version      = "20190802"
}
