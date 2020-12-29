# Serverless + Flask

[The Official Guide to Serverless Flask](https://www.serverless.com/flask)

### Install Serverless framework & plugins

```
npm install -g serverless serverless-wsgi serverless-python-requirements
npm install -g serverless-localstack
```

### Run Flask app locally

```
pipenv install

# we will only need boto3 for local development
pipenv run pip3 install boto3

sls wsgi serve
```

### Deploy to localstack

```
docker-compose up -d
sls deploy --stage local
```

To verify:
```
awslocal lambda list-functions
awslocal apigateway get-rest-apis
```

To test (you will need to use API Gateway ID from the previous command):
```
curl http://localhost:4566/restapis/0nysofyhsh/local/_user_request_/hello/vova
```

### Deploy to AWS
```
sls deploy --stage dev
```
