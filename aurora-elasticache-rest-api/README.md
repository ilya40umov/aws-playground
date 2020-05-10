#### Simple REST API (MySQL / Redis)

A flask app that is MySQL / Redis for storing / caching TODOs.
The app can be used to test AWS Aurora / ElastiCache.

##### Running on EC2 instance

```
sudo yum -y update
sudo yum -y install git python3
pip3 install --user pipenv

git clone https://github.com/ilya40umov/aws-basics/
cd aws-basics/aurora-elasticache-rest-api
pipenv sync

export SQLALCHEMY_DATABASE_URI='mysql+pymysql://user:password@rds-url:3306/todo'
export CACHE_REDIS_HOST='elasticach-redis-url'
export CACHE_REDIS_PORT=6379

pipenv run app_server.py
```

##### Accessing MySQL / Redis via CLI on AWS

To install redis-cli:
```
sudo yum install -y gcc wget
wget http://download.redis.io/redis-stable.tar.gz && tar xvzf redis-stable.tar.gz && cd redis-stable && make
sudo cp src/redis-cli /usr/bin/
```

To install MySQL client:
```
sudo yum install -y https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm
sudo yum install -y mysql-community-client
```
