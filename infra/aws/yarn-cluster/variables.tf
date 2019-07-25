variable "name" {}
variable "subnet_id" {}

# number of workers
variable "workers" {}

# We enforce cert-based authentication for SSH access. Therefore key_name is not
# specified, and this must be specified instead.
variable "ssh_user_data" {}

# config bucket to put the yaml file
variable "s3_config_bucket" {}

variable "bai_version" {
  default = "1.2.5"
}

variable "yarn_worker_memory" {
  default = "140000"
}

variable "installer_version" {
  default = "1.3.0-SNAPSHOT"
}

# If empty, the security group named "infrastructure-allow_all" in the VPC will be used.
variable "security_group_ids" {
  type    = "list"
  default = []
}

# Name of the instance profile to assign to instances. Ignored if empty.
variable "instance_profile" {
  default = ""
}

variable "domain" {
  default = ""
}

variable "route53_zone_name" {
  default = "arimo.com."
}

# Must be a private zone in the VPC of the subnet specified above.
variable "route53_internal_zone_name" {
  default = "arimo.internal."
}

variable "instance_type" {
  type    = "string"
  default = "m5.2xlarge"
}

variable "master_instance_type" {
  type    = "string"
  default = "m5.large"
}

variable "master_ebs_optimized" {
  default = false
}

variable "master_ebs_size" {
  default = 256
}

variable "worker_ebs_optimized" {
  default = true
}

variable "worker_ebs_size" {
  default = 192
}

variable "project_tag" {
  default = "ARIMO"
}

variable "environment_tag" {
  default = "DEV"
}

# Set to true to give workers internal DNS records (not very useful except when we need
# to troubleshoot stuff).
variable "worker_internal_dns" {
  default = false
}

variable "ami_id" {
  # nvidia-version=390.48 nvidia-docker=1
  default = "ami-0a153c414ff639e55"
}

variable "cluster_version" {
  default = 0
}
