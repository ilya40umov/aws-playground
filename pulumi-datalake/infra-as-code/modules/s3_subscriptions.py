import json
import pulumi
from pulumi import Output
from pulumi_aws import s3, lambda_, cloudwatch, iam
from modules.s3_buckets import S3Buckets
from modules.csv2parquet_lambda import Csv2ParquetLambda
from modules.csv2parquet_step_fun import Csv2ParquetStepFunction


class S3Subscriptions(object):
    def __init__(
        self,
        s3_buckets: S3Buckets,
        csv2parquet_lambda: Csv2ParquetLambda,
        csv2parquet_step_fun: Csv2ParquetStepFunction,
    ):
        self.raw_bucket_notification = s3.BucketNotification(
            "RawBucketNotifications",
            bucket=s3_buckets.raw_zone_bucket,
            eventbridge=True,  # send object-level notifications to event bridge
        )
        self.__subscribe_lambda_to_raw_bucket(
            lambda_function_arn=csv2parquet_lambda.lambda_function.arn,
            raw_zone_bucket_name=s3_buckets.raw_zone_bucket.bucket,
            filter_prefix="manual_uploads/",
            filter_suffix=".csv",
        )
        self.__subscribe_step_function_to_raw_bucket(
            step_function_arn=csv2parquet_step_fun.state_machine.arn,
            raw_zone_bucket_name=s3_buckets.raw_zone_bucket.bucket,
            filter_prefix="manual_uploads_v2/",
        )

    @staticmethod
    def __subscribe_lambda_to_raw_bucket(
        lambda_function_arn: Output[str],
        raw_zone_bucket_name: Output[str],
        filter_prefix: str,
        filter_suffix: str,
    ):
        on_object_created_rule = cloudwatch.EventRule(
            "RawZoneObjectCreatedLambdaRule",
            description=f"Raw Zone :: Object Created :: {filter_prefix}*",
            event_pattern=raw_zone_bucket_name.apply(
                lambda bucket_name: json.dumps(
                    {
                        "source": ["aws.s3"],
                        "detail-type": ["Object Created"],
                        "detail": {
                            "bucket": {"name": [bucket_name]},
                            "object": {"key": [{"prefix": filter_prefix}, {"suffix": filter_suffix}]},
                        },
                    }
                )
            ),
        )
        allow_event_bridge_to_exec_lambda = lambda_.Permission(
            "AllowEventBridgeToExecuteLambda",
            action="lambda:InvokeFunction",
            function=lambda_function_arn,
            principal="events.amazonaws.com",
            source_arn=on_object_created_rule.arn,
        )
        event_target = cloudwatch.EventTarget(
            "RawZoneObjectCreatedLambdaTarget",
            rule=on_object_created_rule.name,
            arn=lambda_function_arn,
        )

    @staticmethod
    def __subscribe_step_function_to_raw_bucket(
        step_function_arn: Output[str],
        raw_zone_bucket_name: Output[str],
        filter_prefix: str,
    ):
        event_bridge_role = iam.Role(
            "ExecuteStepFunctionRole",
            assume_role_policy=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"Service": "events.amazonaws.com"},
                            "Action": "sts:AssumeRole",
                        }
                    ],
                }
            ),
        )
        event_bridge_role_policy = iam.RolePolicy(
            "ExecuteStepFunctionRolePolicy",
            role=event_bridge_role.id,
            policy=step_function_arn.apply(
                lambda sfn_arn: json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Action": ["states:StartExecution"],
                                "Resource": sfn_arn,
                            }
                        ],
                    }
                )
            ),
        )
        on_object_created_rule = cloudwatch.EventRule(
            "RawZoneObjectCreatedStepFunctionRule",
            description=f"Raw Zone :: Object Created :: {filter_prefix}*",
            event_pattern=raw_zone_bucket_name.apply(
                lambda bucket_name: json.dumps(
                    {
                        "source": ["aws.s3"],
                        "detail-type": ["Object Created"],
                        "detail": {
                            "bucket": {"name": [bucket_name]},
                            "object": {"key": [{"prefix": filter_prefix}]},
                        },
                    }
                )
            ),
        )
        sns = cloudwatch.EventTarget(
            "RawZoneObjectCreatedStepFunctionTarget",
            rule=on_object_created_rule.name,
            arn=step_function_arn,
            role_arn=event_bridge_role.arn,
        )
