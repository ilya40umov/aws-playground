import json
import pulumi
from pulumi import Output
from pulumi_aws import lambda_, sfn, iam
from modules.csv2parquet_lambda import Csv2ParquetLambda
from modules.sns_topics import SnsTopics


class Csv2ParquetStepFunction(object):
    def __init__(self, csv2parquet_lambda: Csv2ParquetLambda, sns_topics: SnsTopics):
        self.step_function_role = iam.Role(
            "Csv2ParquetStateFunctionRole",
            assume_role_policy=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {
                                "Service": "states.eu-central-1.amazonaws.com"
                            },
                            "Action": "sts:AssumeRole",
                        }
                    ],
                }
            ),
        )
        self.step_function_role_policy = iam.RolePolicy(
            "Csv2ParquetStateFunctionRolePolicy",
            role=self.step_function_role.id,
            policy=Output.all(
                csv2parquet_lambda.lambda_function.arn,
                sns_topics.error_notification_topic.arn,
            ).apply(lambda arns: self.__inline_role_policy(*arns)),
        )
        self.state_machine = sfn.StateMachine(
            "Csv2ParquetStateMachine",
            role_arn=self.step_function_role.arn,
            definition=Output.all(
                csv2parquet_lambda.lambda_function.arn,
                sns_topics.error_notification_topic.arn,
            ).apply(lambda arns: self.__state_machine_definition(*arns)),
        )

    @staticmethod
    def __inline_role_policy(csv2parquet_lambda_arn: str, error_topic_arn: str):
        return json.dumps(
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": ["lambda:InvokeFunction"],
                        "Resource": csv2parquet_lambda_arn,
                    },
                    {
                        "Effect": "Allow",
                        "Action": ["sns:Publish"],
                        "Resource": error_topic_arn,
                    },
                ],
            }
        )

    @staticmethod
    def __state_machine_definition(csv2parquet_lambda_arn: str, error_topic_arn: str):
        return json.dumps(
            {
                "Comment": "Workflow for converting CSV file to Parquet and putting it into the clean zone",
                "StartAt": "CheckFileExtension",
                "States": {
                    "CheckFileExtension": {
                        "Type": "Choice",
                        "Choices": [
                            {
                                "Variable": "$.detail.object.key",
                                "StringMatches": "*.csv",
                                "Next": "Csv2ParquetLambda",
                            }
                        ],
                        "Default": "UnsupportedFileExtension",
                    },
                    "Csv2ParquetLambda": {
                        "Type": "Task",
                        "Resource": "arn:aws:states:::lambda:invoke",
                        "OutputPath": "$.Payload",
                        "Parameters": {
                            "Payload.$": "$",
                            "FunctionName": csv2parquet_lambda_arn,
                        },
                        "Catch": [
                            {
                                "ErrorEquals": ["States.ALL"],
                                "Next": "SnsPublish",
                                "ResultPath": "$.Payload",
                            }
                        ],
                        "Next": "Success",
                    },
                    "Success": {"Type": "Succeed"},
                    "UnsupportedFileExtension": {
                        "Type": "Pass",
                        "Result": {"Error": "InvalidFileFormat"},
                        "Next": "SnsPublish",
                        "ResultPath": "$.Payload",
                    },
                    "SnsPublish": {
                        "Type": "Task",
                        "Resource": "arn:aws:states:::sns:publish",
                        "Parameters": {
                            "TopicArn": error_topic_arn,
                            "Message.$": "$",
                        },
                        "Next": "Fail",
                    },
                    "Fail": {"Type": "Fail"},
                },
            }
        )
