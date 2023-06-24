import pulumi
from pulumi import Output
from pulumi_aws import s3, lambda_


class S3Buckets(object):
    def __init__(self):
        self.raw_zone_bucket = s3.Bucket("raw-zone")
        self.clean_zone_bucket = s3.Bucket("clean-zone")
        self.curated_zone_bucket = s3.Bucket("curated-zone")

    def subscribe_lambda_to_raw_bucket(self, lambda_arn: Output[str], filter_prefix: str, filter_suffix: str):
        allow_bucket_to_exec_lambda = lambda_.Permission(
            "AllowRawBucketToExecuteLambda",
            action="lambda:InvokeFunction",
            function=lambda_arn,
            principal="s3.amazonaws.com",
            source_arn=self.raw_zone_bucket.arn,
        )
        s3.BucketNotification(
            "OnMatchinCsvFileCreatedInRawBucket",
            opts=pulumi.ResourceOptions(depends_on=[allow_bucket_to_exec_lambda]),
            bucket=self.raw_zone_bucket,
            lambda_functions=[
                s3.BucketNotificationLambdaFunctionArgs(
                    lambda_function_arn=lambda_arn,
                    events=["s3:ObjectCreated:*"],
                    filter_prefix=filter_prefix,
                    filter_suffix=filter_suffix
                )
            ],
        )
