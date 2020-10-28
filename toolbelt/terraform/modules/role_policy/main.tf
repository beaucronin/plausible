variable "role_id" {
    type = string
}

variable "actions" {
    type = list(string)
}

variable "resource" {
    default = "*"
}

resource "aws_iam_role_policy" "p" {
    role = var.role_id

    policy = <<-EOF
{
"Version": "2012-10-17",
"Statement": [
    {
    "Action": [
        ${join(",", var.actions)}
    ],
    "Effect": "Allow",
    "Resource": "${var.resource}"
    }
]
}
EOF
}

output "id" {
    value = aws_iam_role_policy.p.id
}