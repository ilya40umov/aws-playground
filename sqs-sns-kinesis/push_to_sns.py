#!/bin/env python3

import boto3
import argparse


parser = argparse.ArgumentParser(description='Push messages to a SNS topic.')
parser.add_argument('--topic-arn', dest='topic_arn', type=str, required=True)
parser.add_argument('--localstack', action='store_const', const=True)

args = parser.parse_args()

if args.localstack:
    print("Using localstack...")
    import localstack_client.session
    session = localstack_client.session.Session()
    sns = session.client('sns')
else:
    sns = boto3.client('sns', region_name='eu-west-1')

dialog = "Type message (press Enter to exit): "

try:
    message = input(dialog)
    while message:
        sns.publish(TopicArn=args.topic_arn, Subject="push_to_sns.py", Message=message)
        message = input(dialog)
except KeyboardInterrupt:
    print("Caught a keyboard interrupt. Stopping...")
