variable "principal" {
    type = string
}

variable "prefix" {
    type = string
}

resource "aws_iam_role" "r" {
    name_prefix = var.prefix

     assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "${var.principal}.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

output "arn" {
    value = aws_iam_role.r.arn
}

output "id" {
    value = aws_iam_role.r.id
}