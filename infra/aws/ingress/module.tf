# TODO: this is duplicated with Devops repo

# - Assumes the LB already has a HTTPS listener.
# - Registers a listener rule in the given LB, pointing to the specified instances.
# - Adds a DNS record to the given zone.
# - Assumes the domain to be served is a sub-domain, for which the listener has the appropriate cert (e.g. wild-card).
#
# Example usage:
#
# module "ingress-docker-portus" {
#   source = "./ingress"
#   load_balancer_name = "infra"
#   zone_id            = "${aws_route53_zone.arimo_com.zone_id}"
#   domain_prefix      = "portus"
#   instances          = ["${aws_instance.docker_portus.id}"]
# }

variable "load_balancer_name" {}

variable "zone_id" {}

variable "domain_prefix" {}

variable "target_type" {
  default = "instance"
}

# FIX: Rename this into 'targets'
variable "instances" {
  type = "list"
}

variable "instance_count" {
}


variable "port" {
  default = 80
}

# Name of the target group. If not given, domain prefix is used.
variable "name" {
  default = ""
}

data "aws_lb" "ingress" {
  name = "${var.load_balancer_name}"
}

data "aws_lb_listener" "https" {
  load_balancer_arn = "${data.aws_lb.ingress.arn}"
  port              = 443
}

data "aws_route53_zone" "external" {
  zone_id = "${var.zone_id}"
}

resource "aws_lb_listener_rule" "main" {
  listener_arn = "${data.aws_lb_listener.https.arn}"

  action {
    type             = "forward"
    target_group_arn = "${aws_lb_target_group.main.arn}"
  }

  condition {
    field  = "host-header"
    values = ["${aws_route53_record.external.name}"]
  }
}

resource "aws_lb_target_group" "main" {
  # XXX FIX
  name        = "${var.name == "" ? var.domain_prefix : var.name}"
  port        = "${var.port}"
  protocol    = "HTTP"
  vpc_id      = "${data.aws_lb.ingress.vpc_id}"
  target_type = "${var.target_type}"

  # TODO: Don't assume 1 instance.
  health_check {
    path                = "/"
    healthy_threshold   = 2
    unhealthy_threshold = 5
    interval            = 60
    timeout             = 5
    matcher             = "200-499"
  }
}

resource "aws_lb_target_group_attachment" "main" {
  count            = "${var.instance_count}"
  target_group_arn = "${aws_lb_target_group.main.arn}"
  target_id        = "${element(var.instances, count.index)}"
}

# TODO: Consider using alias A record instead.
resource "aws_route53_record" "external" {
  zone_id = "${data.aws_route53_zone.external.zone_id}"
  name    = "${var.domain_prefix}.${data.aws_route53_zone.external.name}"
  type    = "CNAME"
  ttl     = 300
  records = ["${data.aws_lb.ingress.dns_name}"]
}

output "domain" {
  value = "${aws_route53_record.external.name}"
}

output "lb_listener_arn" {
  value = "${data.aws_lb_listener.https.arn}"
}
