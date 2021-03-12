locals {
  domain = "${var.domain != "" ? var.domain : "yarn-${var.name}"}"

  public_domain   = "${local.domain}.h1st.com"
  internal_domain = "${local.domain}.h1st.internal"
}

data "template_cloudinit_config" "master" {
  part {
    filename     = "ssh-ca.yml"
    content_type = "text/cloud-config"
    content      = "${var.ssh_user_data}"
  }

  part {
    filename     = ""
    content_type = "text/x-shellscript"
    content      = "${data.template_file.master_init.rendered}"
  }
}

data "template_cloudinit_config" "slave" {
  part {
    filename     = "ssh-ca.yml"
    content_type = "text/cloud-config"
    content      = "${var.ssh_user_data}"
  }

  part {
    filename     = ""
    content_type = "text/x-shellscript"
    content      = "${data.template_file.slave_init.rendered}"
  }
}

resource "aws_network_interface" "master" {
  subnet_id         = "${data.aws_subnet.dev.id}"
  security_groups   = var.security_group_ids
  source_dest_check = false

  tags = {
    Environment = "${var.environment_tag}"
    Project     = "${var.project_tag}"
    Name        = "Yarn ${var.name} master"
  }
}

resource "aws_route53_record" "yarn_master_internal" {
  zone_id = "${data.aws_route53_zone.internal.id}"
  name    = "${local.internal_domain}"

  type    = "A"
  ttl     = "60"
  records = ["${aws_instance.master.private_ip}"]
}

resource "aws_instance" "master" {
  ami           = "${var.ami_id}"
  instance_type = "${var.master_instance_type}"

  # subnet_id              = "${data.aws_subnet.dev.id}"
  # vpc_security_group_ids = ["${var.security_group_ids}"]
  # source_dest_check      = false
  iam_instance_profile = "${length(var.instance_profile) > 0 ? var.instance_profile : ""}"

  ebs_optimized = "${var.master_ebs_optimized}"
  user_data     = "${data.template_cloudinit_config.master.rendered}"

  root_block_device {
    volume_type = "gp2"
    volume_size = "${var.master_ebs_size}"
  }

  volume_tags  = {
    Environment = "${var.environment_tag}"
    Project     = "${var.project_tag}"
  }

  network_interface {
    network_interface_id = "${aws_network_interface.master.id}"
    device_index         = 0
  }

  tags = {
    Environment   = "${var.environment_tag}"
    Project       = "${var.project_tag}"
    Name          = "yarn-${var.name}-master"
    pi-cluster    = "yarn-${var.name}"
    cluster-group = "${var.project_tag}"
    instance-role = "master"                        # should not be required
    domain        = "${lower(local.public_domain)}"
  }

  lifecycle {
    ignore_changes = ["ami"]
  }
}

resource "aws_instance" "workers" {
  ami                    = "${var.ami_id}"
  count                  = "${var.workers}"
  instance_type          = "${var.instance_type}"
  subnet_id              = "${data.aws_subnet.dev.id}"
  vpc_security_group_ids = var.security_group_ids
  iam_instance_profile   = "${length(var.instance_profile) > 0 ? var.instance_profile : ""}"
  source_dest_check      = false
  ebs_optimized          = "${var.worker_ebs_optimized}"
  user_data              = "${data.template_cloudinit_config.slave.rendered}"

  root_block_device {
    volume_type = "gp2"
    volume_size = "${var.worker_ebs_size}"
  }

  volume_tags = {
    Environment = "${var.environment_tag}"
    Project     = "${var.project_tag}"
  }

  tags = {
    Environment   = "${var.environment_tag}"
    Project       = "${var.project_tag}"
    Name          = "yarn-${var.name}-worker-${count.index}"
    pi-cluster    = "yarn-${var.name}"
    cluster-group = "${var.project_tag}"
    instance-role = "slave"                                  # should not be required
  }

  lifecycle {
    ignore_changes = ["ami"]
  }
}

module "ingress" {
  source = "./../ingress"
  name   = "yarn-${lower(var.name)}"

  load_balancer_name = "infra"
  zone_id            = "${data.aws_route53_zone.external.id}"
  domain_prefix      = "${lower(var.domain)}"
  instances          = ["${aws_instance.master.id}"]
  instance_count     = 1
}
