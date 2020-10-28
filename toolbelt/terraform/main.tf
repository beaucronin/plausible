provider "aws" {
    region = "us-west-2"
}

module "role" {
    source = "./modules/role"

    principal = "lambda"
    prefix = "transformer"
}

module "role_policy" {
    source = "./modules/role_policy"
    
    role_id = module.role.id
    actions = ["\"lambda:invokeFunction\""]
    resource = "*"
}

resource "aws_lambda_function" "transformer" {
    filename = "../transformer/lambda.zip"
    function_name = "jsonata-transformer"
    handler = "index.handler"

    runtime = "nodejs12.x"
    role = module.role.arn
}