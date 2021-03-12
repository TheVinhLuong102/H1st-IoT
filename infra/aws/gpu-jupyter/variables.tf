variable "name" {}
variable "subnet_id" {}

# We enforce cert-based authentication for SSH access. Therefore key_name is not
# specified, and this must be specified instead.
variable "ssh_user_data" {}

# If empty, the security group named "infrastructure-allow_all" in the VPC will be used.
variable "security_group_ids" {
  type    = list
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
  default = "h1st.com."
}

# Must be a private zone in the VPC of the subnet specified above.
variable "route53_internal_zone_name" {
  default = "h1st.internal."
}

variable "instance_type" {
  type    = "string"
  default = "m5.2xlarge"
}

variable "ebs_optimized" {
  default = true
}

variable "ebs_size" {
  default = 256
}

variable "project_tag" {
  default = "h1st"
}

variable "environment_tag" {
  default = "DEV"
}

variable "ami_id" {
  # nvidia-version=396.54 nvidia-docker=2
  default = "ami-027b7a641f3860854"
}

data "aws_subnet" "main" {
  id = "${var.subnet_id}"
}

data "aws_route53_zone" "external" {
  name = "h1st.com"
}
