module "yarn-medium" {
  source             = "./yarn-cluster"
  name               = "${var.project_tag}-medium"
  domain             = "yarn-${var.project_tag}-medium.jp"
  subnet_id          = var.subnet1_id
  security_group_ids = [var.internal_security_group_id]
  instance_profile   = aws_iam_instance_profile.yarn.name

  ssh_user_data    = module.ssh.user_data
  s3_config_bucket = var.storage_bucket_name

  # TODO : support ebs for master node

  workers              = 1
  instance_type        = "c5.9xlarge"
  master_instance_type = "m5.2xlarge"
  yarn_worker_memory   = "70000"
  project_tag          = var.project_tag
  environment_tag      = var.environment_tag

  cluster_version      = "20190729"
}

module "yarn-large" {
  source             = "./yarn-cluster"
  name               = "${var.project_tag}-large"
  domain             = "yarn-${var.project_tag}-large.jp"
  subnet_id          = var.subnet1_id
  security_group_ids = [var.internal_security_group_id]
  instance_profile   = aws_iam_instance_profile.yarn.name

  ssh_user_data    = module.ssh.user_data
  s3_config_bucket = var.storage_bucket_name

  # TODO : support ebs for master node

  workers              = 1
  instance_type        = "c5.18xlarge"
  master_instance_type = "m5.2xlarge"
  yarn_worker_memory   = "145000"
  project_tag          = var.project_tag
  environment_tag      = var.environment_tag

  cluster_version      = "20190729"
}

module "yarn-xlarge" {
  source             = "./yarn-cluster"
  name               = "${var.project_tag}-xlarge"
  domain             = "yarn-${var.project_tag}-xlarge.jp"
  subnet_id          = var.subnet1_id
  security_group_ids = [var.internal_security_group_id]
  instance_profile   = aws_iam_instance_profile.yarn.name

  ssh_user_data    = module.ssh.user_data
  s3_config_bucket = var.storage_bucket_name

  # TODO : support ebs for master node

  workers              = 3
  instance_type        = "c5.9xlarge"
  master_instance_type = "m5.2xlarge"
  yarn_worker_memory   = "70000"
  project_tag          = var.project_tag
  environment_tag      = var.environment_tag

  cluster_version      = "20190729"
}

module "yarn-xxlarge" {
  source             = "./yarn-cluster"
  name               = "${var.project_tag}-xxlarge"
  domain             = "yarn-${var.project_tag}-xxlarge.jp"
  subnet_id          = var.subnet1_id
  security_group_ids = [var.internal_security_group_id]
  instance_profile   = aws_iam_instance_profile.yarn.name

  ssh_user_data    = module.ssh.user_data
  s3_config_bucket = var.storage_bucket_name

  # TODO : support ebs for master node

  workers              = 9
  instance_type        = "c5.18xlarge"
  master_instance_type = "m5.2xlarge"
  yarn_worker_memory   = "70000"
  project_tag          = var.project_tag
  environment_tag      = var.environment_tag

  cluster_version      = "20190729"
}
