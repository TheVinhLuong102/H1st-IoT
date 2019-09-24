module "jupyter-alpha" {
  source = "./gpu-jupyter"

  name               = "jupyter-alpha"
  subnet_id          = var.subnet1_id
  security_group_ids = [var.internal_security_group_id]
  instance_profile   = aws_iam_instance_profile.yarn.name
  ssh_user_data      = module.ssh.user_data

  instance_type = "g3.16xlarge"

  domain = "jupyter-alpha.jp"
}

module "jupyter-beta" {
  source = "./gpu-jupyter"

  name               = "jupyter-beta"
  subnet_id          = var.subnet1_id
  security_group_ids = [var.internal_security_group_id]
  instance_profile   = aws_iam_instance_profile.yarn.name
  ssh_user_data      = module.ssh.user_data

  instance_type = "g3.16xlarge"

  domain = "jupyter-beta.jp"
}

module "jupyter-gamma" {
  source = "./gpu-jupyter"

  name               = "jupyter-gamma"
  subnet_id          = var.subnet1_id
  security_group_ids = [var.internal_security_group_id]
  instance_profile   = aws_iam_instance_profile.yarn.name
  ssh_user_data      = module.ssh.user_data

  instance_type = "g3.16xlarge"

  domain = "jupyter-gamma.jp"
}

module "jupyter-delta" {
  source = "./gpu-jupyter"

  name               = "jupyter-delta"
  subnet_id          = var.subnet1_id
  security_group_ids = [var.internal_security_group_id]
  instance_profile   = aws_iam_instance_profile.yarn.name
  ssh_user_data      = module.ssh.user_data

  instance_type = "g3.16xlarge"

  domain = "jupyter-delta.jp"
}

module "jupyter-epsilon" {
  source = "./gpu-jupyter"

  name               = "jupyter-epsilon"
  subnet_id          = var.subnet1_id
  security_group_ids = [var.internal_security_group_id]
  instance_profile   = aws_iam_instance_profile.yarn.name
  ssh_user_data      = module.ssh.user_data

  instance_type = "g3.16xlarge"

  domain = "jupyter-epsilon.jp"
}
