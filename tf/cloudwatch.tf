#####################################################
# Cloudwatch rule
#####################################################
resource "aws_cloudwatch_event_rule" "weekly" {
  name = "weekly_spotify_analysis"
  description = "Trigger weekly"
  schedule_expression = "rate(7 days)"
  is_enabled = true
  tags = {
    Project = local.project
  }
}

resource "aws_cloudwatch_event_target" "lambda" {
  target_id = "spotify_analysis"
  rule = "${aws_cloudwatch_event_rule.weekly.name}"
  arn = "${aws_lambda_function.spotify_analysis.arn}"
}

resource "aws_lambda_permission" "allow_cloudwatch_to_trigger_lambda" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.spotify_analysis.function_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.weekly.arn
}

