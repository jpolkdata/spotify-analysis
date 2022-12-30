#####################################################
# Lambda Function
#####################################################
resource "aws_lambda_function" "spotify_analysis" {
  function_name = "spotify-analysis"
  # layers = [
  #   data.aws_lambda_layer_version.aws_sdk.arn,
  #   data.aws_lambda_layer_version.requests_library.arn
  # ]
  filename = data.archive_file.lambda_deployment.output_path
  handler = "get_album_lengths_from_playlist.lambda_handler"
  role = "${aws_iam_role.lambda_execution_role.arn}"
  runtime = "python3.8"
  timeout = 300

  environment {
    variables = {
      SPOTIPY_CLIENT_ID = var.SPOTIPY_CLIENT_ID,
      SPOTIPY_CLIENT_SECRET = var.SPOTIPY_CLIENT_SECRET
    }
  }
}

#####################################################
# Lambda Layers
#####################################################
# resource "aws_s3_bucket_object" "object" {
#   bucket = aws_s3_bucket.spotify_bucket
#   key    = "new_object_key"
#   source = "path/to/file"

#   # The filemd5() function is available in Terraform 0.11.12 and later
#   # For Terraform 0.11.11 and earlier, use the md5() function and the file() function:
#   # etag = "${md5(file("path/to/file"))}"
#   etag = filemd5("path/to/file")
# }

# data "aws_lambda_layer_version" "lambda_layer_requests" {
#   filename            = "../deployment/layer_requests.zip"
#   layer_name          = "python3-8-requests"
#   # source_code_hash    = data.archive_file.lambda_layer_requests.output_base64sha256 # TODO: save the zip to s3
#   compatible_runtimes = ["python3.8"]
# }

# data "aws_lambda_layer_version" "lambda_layer_spotipy" {
#   filename            = "../deployment/layer_spotipy.zip"
#   layer_name          = "python3-8-spotipy"
#   # source_code_hash    = data.archive_file.lambda_layer_spotipy.output_base64sha256 # TODO: save the zip to s3
#   compatible_runtimes = ["python3.8"]
# }

#####################################################
# IAM Role and Policies
#####################################################
resource "aws_iam_role" "lambda_execution_role" {
  name = "spotify_analysis"
  assume_role_policy = data.aws_iam_policy_document.lambda_trust_policy.json
}

data "aws_iam_policy_document" "lambda_trust_policy" {
  statement {
    actions = [ 
      "sts:AssumeRole"
    ]
    principals {
      type = "Service"
      identifiers = [
        "lambda.amazonaws.com",
        "ec2.amazonaws.com"
      ]
    }
    effect = "Allow"
  }
}

data "aws_iam_policy_document" "lambda_execution_policy_document" {
  statement {
    sid = "ManageLambdaFunction"
    effect = "Allow"
    actions = [
      "lambda:*", # TODO: restrict these permissions to just what is required
      "ec2:*",
      "cloudwatch:*",
      "logs:*",
      "s3:*"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "lambda_execution_policy" {
  name = "lambda_execution_policy"
  policy = data.aws_iam_policy_document.lambda_execution_policy_document.json
}

resource "aws_iam_role_policy_attachment" "lambda_execution_attachment" {
  role = aws_iam_role.lambda_execution_role.name
  policy_arn = aws_iam_policy.lambda_execution_policy.arn
}

