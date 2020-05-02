#### ASG scaling on custom metric

App for testing ASG scaling based on a custom metric.

##### Development

```
python3 -m virtualenv -p python3 .venv
source .venv/bin/activate
pip3 install -r requirements.txt

docker-compose up

python3 -m flask run
```

##### EC2 User Data

```
#!/bin/bash

cd /opt
mkdir app
cd app
git clone https://github.com/ilya40umov/aws-basics
cd aws-basics/asg-custom-metric-policy
pip3 install -r requirements.txt
python3 waitress_server.py 
```
