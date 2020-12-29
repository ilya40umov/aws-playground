import os

import boto3

localstack_hostname = os.environ['LOCALSTACK_HOSTNAME']

if localstack_hostname:
    dynamodb = boto3.resource('dynamodb', endpoint_url=f"http://{localstack_hostname}:4566")
else:
    dynamodb = boto3.resource('dynamodb')


def delete(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    table.delete_item(
        Key={
            'alias': event['pathParameters']['alias']
        }
    )

    response = {
        "statusCode": 200
    }

    return response
