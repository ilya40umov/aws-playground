# looks like localstack won't deliver messages from SNS topic into a FIFO SQS queue
resource "aws_sqs_queue" "sqs_xyz_queue" {
  name                      = "sqs-xyz-queue"
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 20
}
