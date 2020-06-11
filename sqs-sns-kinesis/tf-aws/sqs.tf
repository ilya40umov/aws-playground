resource "aws_sqs_queue" "sqs_xyz_queue" {
  name                      = "sqs-xyz-queue"
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 20
}

resource "aws_sqs_queue_policy" "sqs_xyz_queue" {
  queue_url = aws_sqs_queue.sqs_xyz_queue.id
  policy    = data.aws_iam_policy_document.sqs_xyz_queue.json 
}

data "aws_iam_policy_document" "sqs_xyz_queue" {
  policy_id = "SqsXyzQueuePolicy"
  statement {
    sid       = "sid001"
    effect    = "Allow"
    actions   = ["sqs:SendMessage"]
    resources = [aws_sqs_queue.sqs_xyz_queue.arn]
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
    condition {
      test     = "ArnEquals"
      variable = "aws:SourceArn"
      values   = [aws_sns_topic.sns_xyz_topic.arn]
    }
  }
  statement {
    sid       = "sid002"
    effect    = "Allow"
    actions   = ["sqs:DeleteMessage", "sqs:ReceiveMessage"]
    resources = [aws_sqs_queue.sqs_xyz_queue.arn]
    principals {
      type        = "AWS"
      identifiers = [aws_iam_role.aim_xyz_ec2_role.arn]
    }
  }
}
