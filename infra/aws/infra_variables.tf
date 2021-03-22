variable "region" {
  default = "ap-northeast-1"
}

variable "storage_bucket_name" {
  default = "h1st-panasonic-ap-jp-cc-pm"
}

variable "vpc_id" {
  default = "vpc-6886010f"
}

variable "subnet1_id" {
  default = "subnet-59421d10" # 1a
}

variable "subnet2_id" {
  default = "subnet-547bf30f" # 1c
}

# common security group to assign to all workers
variable "internal_security_group_id" {
  default = "sg-fb0d2282"
}

variable "project_tag" {
  default = "CCPM"
}

variable "environment_tag" {
  default = "DEV"
}

