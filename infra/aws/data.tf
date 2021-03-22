data "aws_vpc" "main" {
  id = var.vpc_id
}

data "aws_subnet" "subnet1" {
  id = var.subnet1_id
}

data "aws_subnet" "subnet2" {
  id = var.subnet2_id
}

data "aws_caller_identity" "default" {
}

data "aws_region" "default" {
}

data "aws_route53_zone" "external" {
  name = "h1st.com"
}

