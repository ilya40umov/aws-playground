import json
import pulumi
from pulumi import Output
from pulumi_aws import s3, iam, lambda_
from modules.s3_buckets import S3Buckets


class Csv2ParquetLambda(object):
    def __init__(self, s3_buckets: S3Buckets):
        self.lambda_role = iam.Role(
            "CsvToParquetLambdaRole",
            assume_role_policy=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Action": "sts:AssumeRole",
                            "Principal": {"Service": "lambda.amazonaws.com"},
                            "Effect": "Allow",
                            "Sid": "",
                        }
                    ],
                }
            ),
            inline_policies=[
                iam.RoleInlinePolicyArgs(
                    name="CloudWatchAndS3AndGlue",
                    policy=Output.all(
                        s3_buckets.raw_zone_bucket.arn,
                        s3_buckets.clean_zone_bucket.arn,
                    ).apply(self.__create_inline_policy),
                )
            ],
        )
        self.lambda_function = lambda_.Function(
            "CsvToParquetLambda",
            name="CsvToParquetLambda",
            code=pulumi.FileArchive("../csv2parquet/"),
            role=self.lambda_role.arn,
            handler="lambda_function.lambda_handler",
            runtime="python3.10",
            environment=lambda_.FunctionEnvironmentArgs(
                variables=s3_buckets.clean_zone_bucket.bucket.apply(
                    lambda bucket_name: {"OUTPUT_BUCKET": bucket_name}
                ),
            ),
            # see https://aws-sdk-pandas.readthedocs.io/en/stable/layers.html
            layers=[
                "arn:aws:lambda:eu-central-1:336392948345:layer:AWSSDKPandas-Python310:3"
            ],
            timeout=300,
            memory_size=256,
        )

    @staticmethod
    def __create_inline_policy(bucket_arns: list) -> str:
        return json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": [
                            "logs:PutLogEvents",
                            "logs:CreateLogGroup",
                            "logs:CreateLogStream",
                        ],
                        "Resource": "arn:aws:logs:*:*:*",
                    },
                    {
                        "Effect": "Allow",
                        "Action": ["s3:*"],
                        "Resource": bucket_arns + [f"{arn}/*" for arn in bucket_arns],
                    },
                    {"Effect": "Allow", "Action": ["glue:*"], "Resource": "*"},
                ],
            }
        )
