#!/bin/env python3

import boto3
import argparse
import hashlib
import json


parser = argparse.ArgumentParser(description='Receive messages from SQS and push them to Kinesis.')
parser.add_argument('--queue-url', dest='queue_url', type=str, required=True)
parser.add_argument('--stream-name', dest='stream_name', type=str, required=True)
parser.add_argument('--localstack', action='store_const', const=True)

args = parser.parse_args()

if args.localstack:
    print("Using localstack...")
    import localstack_client.session
    session = localstack_client.session.Session()
    sqs = session.client('sqs')
    kinesis = session.client('kinesis')
else:
    sqs = boto3.client('sqs', region_name='eu-west-1')
    kinesis = boto3.client('kinesis', region_name='eu-west-1')

try:
    while True:
        sqs_response = sqs.receive_message(
            QueueUrl=args.queue_url,
            AttributeNames=['SentTimestamp'],
            MaxNumberOfMessages=1,
	    MessageAttributeNames=['All'],
	    VisibilityTimeout=60,
	    WaitTimeSeconds=5
        )
        
        if 'Messages' not in sqs_response:
            continue

        envelope = sqs_response['Messages'][0]
        payload = json.loads(envelope['Body'])
        receipt_handle = envelope['ReceiptHandle']
        message = payload['Message'] # the actual message that was pushed to SNS

        print(f"Relaying into Kinesis: '{message}'")
        md5 = hashlib.md5()
        md5.update(message.encode('utf-8'))
        partition_key = md5.hexdigest()
        kinesis.put_record(
            StreamName=args.stream_name,
            Data=json.dumps({'Message': message}),
            PartitionKey=partition_key
	)
	
        sqs.delete_message(
            QueueUrl=args.queue_url,
            ReceiptHandle=receipt_handle
        )
except KeyboardInterrupt:
    print("Caught a keyboard interrupt. Stopping...")
