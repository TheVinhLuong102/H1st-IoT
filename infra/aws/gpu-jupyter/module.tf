locals {
  cluster = "${var.name}-jupyter"
}

data "template_file" "init" {
  template = "${file("${path.module}/templates/install.sh")}"

  vars = {}
}

data "template_cloudinit_config" "init" {
  part {
    filename     = "ssh-ca.yml"
    content_type = "text/cloud-config"
    content      = "${var.ssh_user_data}"
  }

  part {
    filename     = ""
    content_type = "text/x-shellscript"
    content      = "${data.template_file.init.rendered}"
  }
}

resource "aws_instance" "master" {
  ami           = var.ami_id
  instance_type = var.instance_type

  subnet_id              = var.subnet_id
  vpc_security_group_ids = var.security_group_ids

  # source_dest_check      = false
  iam_instance_profile = "${length(var.instance_profile) > 0 ? var.instance_profile : ""}"

  ebs_optimized = "${var.ebs_optimized}"
  user_data     = "${data.template_cloudinit_config.init.rendered}"

  root_block_device {
    volume_type = "gp2"
    volume_size = "196"
  }

  volume_tags = {
    Environment = "${var.environment_tag}"
    Project     = "${var.project_tag}"
  }

  tags = {
    Environment   = "${var.environment_tag}"
    Project       = "${var.project_tag}"
    Name          = "${var.name}"
    pi-cluster    = "${var.name}"
    cluster-group = "${var.project_tag}"
    instance-role = "master"                 # should not be required

    domain = "${var.domain}.h1st.com"
  }

  lifecycle {
    ignore_changes = [ami]
  }
}

resource "aws_ebs_volume" "ebs" {
  availability_zone = "${data.aws_subnet.main.availability_zone}"
  size              = "${var.ebs_size}"
  type              = "gp2"

  tags = {
    Name        = "${local.cluster} - EBS"
    Cluster     = "${local.cluster}"
    Vendor      = "h1st"
    Environment = "${var.environment_tag}"
    Project     = "${var.project_tag}"
  }
}

resource "aws_volume_attachment" "ebs_att" {
  device_name = "/dev/xvdh"
  volume_id   = aws_ebs_volume.ebs.id
  instance_id = aws_instance.master.id

  # this may be required for running instance
  force_detach = true
}

module "ingress" {
  source = "./../ingress"
  name   = "${var.name}"

  load_balancer_name = "infra"
  zone_id            = "${data.aws_route53_zone.external.id}"
  domain_prefix      = "${lower(var.domain)}"
  instances          = ["${aws_instance.master.id}"]
  instance_count     = 1
}
