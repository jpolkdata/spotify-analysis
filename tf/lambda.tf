#####################################################
# Lambda function
#####################################################
resource "aws_lambda_function" "spotify_analysis" {
  function_name = "spotify-analysis"
  description   = "generate data about artists from Spotify API"
  layers = [
    aws_lambda_layer_version.lambda_layer_requests.arn,
    aws_lambda_layer_version.lambda_layer_spotipy.arn
  ]
  filename = data.archive_file.lambda_deployment.output_path
  handler = "get_album_lengths_from_playlist.lambda_handler"
  role = "${aws_iam_role.lambda_execute_role.arn}"
  runtime = "python3.8"
  timeout = 300

  source_code_hash = filebase64sha256(data.archive_file.lambda_deployment.output_path)

  environment {
    variables = {
      SPOTIPY_CLIENT_ID = var.SPOTIPY_CLIENT_ID,
      SPOTIPY_CLIENT_SECRET = var.SPOTIPY_CLIENT_SECRET
    }
  }

  tags = {
    Project = local.project
  }
}

#####################################################
# Lambda layers
#####################################################
resource "aws_lambda_layer_version" "lambda_layer_requests" {
  layer_name          = "requests"
  s3_bucket           = "${aws_s3_object.s3_layer_requests.bucket}"
  s3_key              = "${aws_s3_object.s3_layer_requests.key}"
  s3_object_version   = "${aws_s3_object.s3_layer_requests.version_id}"
  compatible_runtimes = ["python3.8"]
}

resource "aws_lambda_layer_version" "lambda_layer_spotipy" {
  layer_name          = "spotipy"
  s3_bucket           = "${aws_s3_object.s3_layer_spotipy.bucket}"
  s3_key              = "${aws_s3_object.s3_layer_spotipy.key}"
  s3_object_version   = "${aws_s3_object.s3_layer_spotipy.version_id}"
  compatible_runtimes = ["python3.8"]
}

#####################################################
# IAM role and policies
#####################################################
resource "aws_iam_role" "lambda_execute_role" {
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

data "aws_iam_policy_document" "lambda_execute_policy_document" {
  statement {
    sid       = "InvokeFunction"
    effect    = "Allow"
    actions   = ["lambda:InvokeFunction"]
    resources = [aws_lambda_function.spotify_analysis.arn]
  }
  statement {
    sid       = "WriteToS3"
    effect    = "Allow"
    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.spotify_data_bucket.arn}/*"]
  }
}

resource "aws_iam_policy" "lambda_execute_policy" {
  name = "lambda_execution_policy"
  policy = data.aws_iam_policy_document.lambda_execute_policy_document.json
}

resource "aws_iam_role_policy_attachment" "lambda_execution_attachment" {
  role = aws_iam_role.lambda_execute_role.name
  policy_arn = aws_iam_policy.lambda_execute_policy.arn
}

