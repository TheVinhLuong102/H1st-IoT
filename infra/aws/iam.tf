data "aws_iam_policy_document" "s3_access" {
  statement {
    actions = ["s3:*"]
    resources = [
      "arn:aws:s3:::h1st-bai/*",
      "arn:aws:s3:::h1st-iot-pm/*",
      "arn:aws:s3:::h1st-panasonic-ap-jp-cc-pm",
      "arn:aws:s3:::h1st-panasonic-ap-jp-cc-pm/*",
      "arn:aws:s3:::h1st-panasonic-ap",
      "arn:aws:s3:::h1st-panasonic-ap/*",
      "arn:aws:s3:::h1st-panasonic-iot-pm",
      "arn:aws:s3:::h1st-panasonic-iot-pm/*",
      "arn:aws:s3:::h1st-bai-clusters/custom_provisioner/ccpm*",
    ]
  }

  statement {
    actions = [
      "s3:GetBucketLocation",
      "s3:ListAllMyBuckets",
    ]

    resources = ["arn:aws:s3:::*"]
  }
}

data "aws_iam_policy_document" "ec2_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "yarn" {
  name               = "${var.project_tag}-yarn"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json
}

resource "aws_iam_instance_profile" "yarn" {
  name = aws_iam_role.yarn.name
  role = aws_iam_role.yarn.name
}

resource "aws_iam_role_policy" "node_s3_policy" {
  name   = "${var.project_tag}-s3-access"
  policy = data.aws_iam_policy_document.s3_access.json
  role   = aws_iam_role.yarn.id
}

