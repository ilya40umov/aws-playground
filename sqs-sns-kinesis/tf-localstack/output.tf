output "xyz_queue_arn" {
  value = aws_sqs_queue.sqs_xyz_queue.arn
}

output "xyz_topic_arn" {
  value = aws_sns_topic.sns_xyz_topic.arn
}

output "xyz_stream_arn" {
  value = aws_kinesis_stream.kinesis_xyz_stream.arn
}
