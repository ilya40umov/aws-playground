resource "aws_iam_role" "aim_xyz_ec2_role" {
  name               = "TestXyzEC2Role"
  assume_role_policy = data.aws_iam_policy_document.aim_xyz_ec2_role_policy_doc.json
}

data "aws_iam_policy_document" "aim_xyz_ec2_role_policy_doc" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_instance_profile" "aim_xyz_ec2_role" {
  name = "xyz_ec2_role"
  role = "${aws_iam_role.aim_xyz_ec2_role.name}"
}

resource "aws_iam_role_policy" "aim_xyz_ec2_role_policy" {
  name = "AllowEC2XyzToWorkWithKinesis"
  role = aws_iam_role.aim_xyz_ec2_role.id

  policy = <<-EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Stmt123",
      "Effect": "Allow",
      "Action": [
        "kinesis:DescribeStream",
        "kinesis:PutRecord",
        "kinesis:PutRecords",
        "kinesis:GetShardIterator",
        "kinesis:GetRecords",
        "kinesis:ListShards",
        "kinesis:DescribeStreamSummary",
        "kinesis:RegisterStreamConsumer"
      ],
      "Resource": [
        "${aws_kinesis_stream.kinesis_xyz_stream.arn}"
      ]
    },
    {
      "Sid": "Stmt234",
      "Effect": "Allow",
      "Action": [
        "kinesis:SubscribeToShard",
        "kinesis:DescribeStreamConsumer"
      ],
      "Resource": [
        "${aws_kinesis_stream.kinesis_xyz_stream.arn}/*"
      ]
    }
  ]
}
  EOF
}
