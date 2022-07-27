resource "aws_lambda_permission" "allow_s3" {
  statement_id  = "S3Execution"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.parse_txt_as_dataset.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_s3_bucket.chats-json.arn
  qualifier     = aws_lambda_alias.parse_alias.name
}

resource "aws_lambda_alias" "parse_alias" {
  name             = "parse_txt"
  description      = "Function that parses a txt file and produces a csv file"
  function_name    = aws_lambda_function.parse_txt_as_dataset.function_name
  function_version = "$LATEST"
}

resource "aws_s3_bucket_notification" "aws-lambda-trigger" {
  bucket = aws_s3_bucket.chats-json.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.parse_txt_as_dataset.arn
    events              = ["s3:ObjectCreated:*"]
  }
}

resource "aws_lambda_function" "parse_txt_as_dataset" {
   architectures                  = [
        "x86_64",
    ]
    function_name                  = "parse_txt_as_dataset"
    handler                        = "parse_txt_as_dataset.parse.handler"
    layers                         = []
    memory_size                    = 128
    package_type                   = "Zip"
    filename = "../metrics/parse.zip"
    source_code_hash = filebase64sha256("../metrics/parse.zip")
    role          = aws_iam_role.iam_for_lambda.arn
    runtime                        = "python3.9"
    timeout                        = 3

    ephemeral_storage {
        size = 512
    }

    timeouts {}

    tracing_config {
        mode = "PassThrough"
    }

}
