module "jupyter-alpha" {
  source = "./gpu-jupyter"

  name               = "jupyter-alpha"
  subnet_id          = var.subnet1_id
  security_group_ids = [var.internal_security_group_id]
  instance_profile   = aws_iam_instance_profile.yarn.name
  ssh_user_data      = module.ssh.user_data

  instance_type = "g3.8xlarge"

  domain = "jupyter-alpha.jp"
}

module "jupyter-beta" {
  source = "./gpu-jupyter"

  name               = "jupyter-beta"
  subnet_id          = var.subnet1_id
  security_group_ids = [var.internal_security_group_id]
  instance_profile   = aws_iam_instance_profile.yarn.name
  ssh_user_data      = module.ssh.user_data

  instance_type = "g3.8xlarge"

  domain = "jupyter-beta.jp"
}

