#### Simple REST API (MySQL / Redis)

A flask app that is MySQL / Redis for storing / caching TODOs.
The app can be used to test AWS Aurora / ElastiCache.

##### Accesing MySQL / Redis via CLI on AWS

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
