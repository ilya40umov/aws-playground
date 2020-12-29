import json
import logging
import os
import time

import boto3

localstack_hostname = os.environ['LOCALSTACK_HOSTNAME']

if localstack_hostname:
    dynamodb = boto3.resource('dynamodb', endpoint_url=f"http://{localstack_hostname}:4566")
else:
    dynamodb = boto3.resource('dynamodb')


def create(event, context):
    data = json.loads(event['body'])
    
    if 'alias' not in data or 'url' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the alias.")
    
    timestamp = str(time.time())

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    item = {
        'alias': data['alias'],
        'url': data['url'],
        'createdAt': timestamp,
        'updatedAt': timestamp
    }

    table.put_item(Item=item)

    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response
