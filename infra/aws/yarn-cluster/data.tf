data "aws_subnet" "dev" {
  id = "${var.subnet_id}"
}

data "aws_route53_zone" "external" {
  name = "${var.route53_zone_name}"
}

data "aws_route53_zone" "internal" {
  name = "${var.route53_internal_zone_name}"
  vpc_id = "${data.aws_subnet.dev.vpc_id}"
}
