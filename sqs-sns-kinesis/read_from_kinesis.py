#!/bin/env python3

import boto3
import argparse
import time


parser = argparse.ArgumentParser(description='Read records from a Kinesis stream.')
parser.add_argument('--stream-name', dest='stream_name', type=str, required=True)
parser.add_argument('--localstack', action='store_const', const=True)

args = parser.parse_args()

if args.localstack:
    print("Using localstack...")
    import localstack_client.session
    session = localstack_client.session.Session()
    kinesis = session.client('kinesis')
else:
    kinesis = boto3.client('kinesis', region_name='eu-west-1')

response = kinesis.describe_stream(StreamName=args.stream_name)
shard_id = response['StreamDescription']['Shards'][0]['ShardId']

shard_iterator_response = kinesis.get_shard_iterator(StreamName=args.stream_name, ShardId=shard_id, ShardIteratorType='TRIM_HORIZON')
shard_iterator = shard_iterator_response['ShardIterator']

record_response = kinesis.get_records(ShardIterator=shard_iterator, Limit=2)

try:
    while 'NextShardIterator' in record_response:
        if record_response['Records']:
            for r in record_response['Records']:
                print(r['Data'])
        else:
            time.sleep(5)
        record_response = kinesis.get_records(ShardIterator=record_response['NextShardIterator'], Limit=2)
except KeyboardInterrupt:
    print("Caught a keyboard interrupt. Stopping...")
