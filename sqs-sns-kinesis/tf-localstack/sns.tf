resource "aws_sns_topic" "sns_xyz_topic" {
  name = "sns-xyz-topic"
}

resource "aws_sns_topic_subscription" "sqs_xyz_queue" {
  topic_arn = aws_sns_topic.sns_xyz_topic.arn
  protocol  = "sqs"
  endpoint  = aws_sqs_queue.sqs_xyz_queue.arn
}
