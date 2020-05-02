#### Report custom metric to CloudWatch

A flask app that is reporting a custom metric to CloudWatch every minute

##### Development

```
python3 -m virtualenv -p python3 .venv
source .venv/bin/activate
pip3 install -r requirements.txt

docker-compose up -d

USE_LOCALSTACK=true python3 -m flask run
```

```
curl http://localhost:5000/
curl -XPOST http://localhost:5000/start_computation
```

##### EC2 User Data

```
#!/bin/bash
yum -y update
yum -y install git python3

cd /opt
mkdir app

cd app
git clone https://github.com/ilya40umov/aws-basics

cd ..
chown ec2-user:ec2-user app
find app -name '*' -exec chown ec2-user:ec2-user {} +
chmod -R 2740 app/

cd app/aws-basics/cloudwatch-custom-metric
pip3 install -r requirements.txt

su ec2-user -c ./run.sh 
```
