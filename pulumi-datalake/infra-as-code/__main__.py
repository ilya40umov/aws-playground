import json
import pulumi
from pulumi import Output
from pulumi_aws import s3, iam, lambda_


class S3Buckets(object):
    def __init__(self):
        self.raw_zone_bucket = s3.Bucket("raw-zone")
        self.clean_zone_bucket = s3.Bucket("clean-zone")
        self.curated_zone_bucket = s3.Bucket("curated-zone")
        self.export_bucket_ids()

    def export_bucket_ids(self):
        pulumi.export("raw-zone-bucket-id", self.raw_zone_bucket.id)
        pulumi.export("clean-zone-bucket-id", self.clean_zone_bucket.id)
        pulumi.export("curated-zone-bucket-id", self.curated_zone_bucket.id)


class CsvToParquetLambda(object):
    def __init__(self, s3_buckets: S3Buckets):
        self.role = iam.Role(
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
                        s3_buckets.curated_zone_bucket.arn,
                    ).apply(self.__create_inline_policy),
                )
            ],
        )
        self.lambda_function = lambda_.Function(
            "CsvToParquetLambda",
            name="CsvToParquetLambda",
            code=pulumi.FileArchive("../csv2parquet/"),
            role=self.role.arn,
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
        self.subscribe_to_raw_bucket(s3_buckets)

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

    def subscribe_to_raw_bucket(self, s3_buckets: S3Buckets):
        allow_bucket = lambda_.Permission(
            "AllowRawBucketToExecuteLambda",
            action="lambda:InvokeFunction",
            function=self.lambda_function.arn,
            principal="s3.amazonaws.com",
            source_arn=s3_buckets.raw_zone_bucket.arn,
        )
        s3.BucketNotification(
            "OnMatchinCsvFileCreatedInRawBucket",
            opts=pulumi.ResourceOptions(depends_on=[allow_bucket]),
            bucket=s3_buckets.raw_zone_bucket,
            lambda_functions=[
                s3.BucketNotificationLambdaFunctionArgs(
                    lambda_function_arn=self.lambda_function.arn,
                    events=["s3:ObjectCreated:*"],
                    filter_prefix="manual_uploads/",
                    filter_suffix=".csv",
                )
            ],
        )


if __name__ == "__main__":
    s3_buckets = S3Buckets()
    csv_to_parquet_lambda = CsvToParquetLambda(s3_buckets)
