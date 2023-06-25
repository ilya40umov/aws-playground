import json
import pulumi
from pulumi_aws import lambda_, sfn, iam
from modules.csv2parquet_lambda import Csv2ParquetLambda


class Csv2ParquetStepFunction(object):
    def __init__(self, csv2parquet_lambda: Csv2ParquetLambda):
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
            policy=csv2parquet_lambda.lambda_function.arn.apply(
                lambda lambda_arn: json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Effect": "Allow",
                                "Action": ["lambda:InvokeFunction"],
                                "Resource": lambda_arn,
                            }
                        ],
                    }
                )
            ),
        )
        self.state_machine = sfn.StateMachine(
            "Csv2ParquetStateMachine",
            role_arn=self.step_function_role.arn,
            definition=csv2parquet_lambda.lambda_function.arn.apply(
                lambda lambda_arn: json.dumps(
                    {
                        "Comment": "Workflow for converting CSV file to Parquet and putting it into the clean zone",
                        "StartAt": "Csv2ParquetLambda",
                        "States": {
                            "Csv2ParquetLambda": {
                                "Type": "Task",
                                "Resource": "arn:aws:states:::lambda:invoke",
                                "OutputPath": "$.Payload",
                                "Parameters": {
                                    "Payload.$": "$",
                                    "FunctionName": lambda_arn,
                                },
                                "End": True,
                            }
                        },
                    }
                )
            ),
        )
