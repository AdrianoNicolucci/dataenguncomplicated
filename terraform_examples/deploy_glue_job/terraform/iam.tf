data "aws_iam_policy_document" "glue_execution_assume_role_policy" {
  statement {
    sid     = ""
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["glue.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "data_lake_policy" {
  #  name        = "EventBridgeLambdaPolicy"
  #  description = "IAM policy for allowing EventBridge to invoke any Lambda function"
  statement {

    effect    = "Allow"
    resources = ["arn:aws:s3:::${var.s3_bucket}/*"]

    actions = ["s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject"]
  }

  statement {
    effect    = "Allow"
    resources = ["arn:aws:s3:::${var.s3_bucket}/",
                 "arn:aws:s3:::awsglue-datasets/"]

    actions = ["s3:ListBucket"]
  }

   statement {
    effect    = "Allow"
    resources = ["arn:aws:s3:::awsglue-datasets/*"]

    actions = ["s3:GetObject"]
  }
}

resource "aws_iam_policy" "data_lake_access_policy" {
  name        = "s3DataLakePolicy-${var.s3_bucket}"
  description = "allows for running glue job in the glue console and access my s3_bucket"
  policy      = data.aws_iam_policy_document.data_lake_policy.json
  tags = {
    Application = var.project
  }
}


resource "aws_iam_role" "glue_service_role" {
name = "aws_glue_job_runner"
assume_role_policy = data.aws_iam_policy_document.glue_execution_assume_role_policy.json
tags = {
Application = var.project
}
}

resource "aws_iam_role_policy_attachment" "data_lake_permissions" {
  role = aws_iam_role.glue_service_role.name
  policy_arn = aws_iam_policy.data_lake_access_policy.arn
}