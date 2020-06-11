#### App to snowcase SQS / SNS / Kinesis

This app is testing a bit unusual set-up,
where messages are sent to an SNS topic,
which puts them into an SQS queue, 
and then those messages are consumed from the SQS queue and put into a Kinesis stream.
Whether this set-up actually makes sense in practice is a different topic, 
as SQS queue is gonna mess up the ordering of the messages, 
and one can't subsribe a FIFO queue to an SNS topic.

##### Local development

Prepare the environment:
```
pipenv install
docker-compose up -d
cd tf-localstack
terraform init
terraform apply
```

To start producing messages run the following commands in the first terminal:
```
pipenv shell
./push_to_sns.py --topic-arn=arn:aws:sns:us-east-1:000000000000:sns-xyz-topic --localstack
```

To start consuming from SQS and putting messages into Kinesis, run the following in the second terminal:
```
pipenv shell
./copy_from_sqs_to_kinesis.py --queue-url=http://localhost:4566/queue/sqs-xyz-queue --stream-name=kinesis-xyz-stream --localstack
```

Finally, to read the data from Kinesis, run the following in the thrid terminal:
```
pipenv shell
./read_from_kinesis.py --stream-name=kinesis-xyz-stream --localstack
```

##### To deploy to AWS

```
cd tf-aws
terraform apply -var="aws_profile=xxyyzz"
```

Create an EC2 instance assuming `TestXyzEC2Role`, ssh into the instance, clone this repo and run the scripts from the previous section (you will need to remove `--localstack` and provide arn/urls of the newly created resources).
