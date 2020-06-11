resource "aws_sns_topic" "sns_xyz_topic" {
  name = "sns-xyz-topic"
}

resource "aws_sns_topic_subscription" "sqs_xyz_queue" {
  topic_arn = aws_sns_topic.sns_xyz_topic.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.sqs_xyz_queue.arn
}

resource "aws_sns_topic_policy" "sns_xyz_topic" {
  arn = aws_sns_topic.sns_xyz_topic.arn
  policy = data.aws_iam_policy_document.sns_xyz_topic.json
}

data "aws_iam_policy_document" "sns_xyz_topic" {
  policy_id = "SnsXyzTopicPolicy"

  statement {
    sid = "sid001"
    effect = "Allow"
    actions = ["SNS:Publish"]
    principals {
      type        = "AWS"
      identifiers = [aws_iam_role.aim_xyz_ec2_role.arn]
    }
    resources = [aws_sns_topic.sns_xyz_topic.arn]
  }
}
