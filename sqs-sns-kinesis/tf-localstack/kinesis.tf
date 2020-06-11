resource "aws_kinesis_stream" "kinesis_xyz_stream" {
  name             = "kinesis-xyz-stream"
  shard_count      = 1
  retention_period = 48
}
