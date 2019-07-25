data "template_file" "master_config" {
  template = "${file("${path.module}/templates/config.master.yaml")}"

  vars = {
    master_node        = "${local.internal_domain}"
    public_url         = "https://${lower(local.public_domain)}"
    yarn_worker_memory = "${var.yarn_worker_memory}"
  }
}

data "template_file" "slave_config" {
  template = "${file("${path.module}/templates/config.slave.yaml")}"

  vars = {
    master_node        = "${local.internal_domain}"
    yarn_worker_memory = "${var.yarn_worker_memory}"
  }
}

resource "aws_s3_bucket_object" "master_config" {
  bucket  = "${var.s3_config_bucket}"
  key     = ".infrastructure/${local.internal_domain}/master.yaml"
  content = "${data.template_file.master_config.rendered}"
}

data "template_file" "master_init" {
  template = "${file("${path.module}/templates/install.sh")}"

  vars = {
    installer_version = "${var.installer_version}"
    config_file       = "s3://${var.s3_config_bucket}/${aws_s3_bucket_object.master_config.id}"
    cluster_version   = "${var.cluster_version}"
  }
}

resource "aws_s3_bucket_object" "slave_config" {
  bucket  = "${var.s3_config_bucket}"
  key     = ".infrastructure/${local.internal_domain}/slave.yaml"
  content = "${data.template_file.slave_config.rendered}"
}

data "template_file" "slave_init" {
  template = "${file("${path.module}/templates/install.sh")}"

  vars = {
    installer_version = "${var.installer_version}"
    config_file       = "s3://${var.s3_config_bucket}/${aws_s3_bucket_object.slave_config.id}"
    cluster_version   = "${var.cluster_version}"
  }
}
