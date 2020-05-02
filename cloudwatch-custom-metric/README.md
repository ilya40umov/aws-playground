#### Report custom metric to CloudWatch

A flask app that is reporting a custom metric to CloudWatch every minute

##### Development

```
python3 -m virtualenv -p python3 .venv
source .venv/bin/activate
pip3 install -r requirements.txt

docker-compose up

USE_LOCALSTACK=true python3 -m flask run
```

```
curl http://localhost:5000/
curl -XPOST http://localhost:5000/start_computation
```

##### EC2 User Data

```
#!/bin/bash
sudo yum -y update
sudo yum -y install git python3
cd /opt
sudo mkdir app
sudo chown ec2-user:ec2-user app
sudo chmod 2770 app/
cd app
git clone https://github.com/ilya40umov/aws-basics
cd aws-basics/asg-custom-metric-policy
sudo pip3 install -r requirements.txt
nohup python3 waitress_server.py 2>&1 & > /dev/null
```
