# ECR & Elastic Beanstalk

### Bulding a simple Docker image and pushing it to ECR

To create an ECR repo one can either use AWS Console or do it via AWS CLI.
E.g. [here](https://docs.aws.amazon.com/cli/latest/reference/ecr/create-repository.html) is a command to create a new repo.

Then to authenticate Docker against the repository, one can use [this command](https://docs.aws.amazon.com/AmazonECR/latest/userguide/Registries.html#registry_auth).

After this is done, you can build and publish the images using the following commands:

```
$ cd image/
$ IMAGE_NAME="..." # e.g. xxxxx.dkr.ecr.eu-west-1.amazonaws.com/apache-php
$ docker build -t $IMAGE_NAME:latest .
$ docker push $IMAGE_NAME:latest
```

### Deploying the image as Elastic Beanstalk app

Overall the instructions from [here](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/single-container-docker.html) should work.
However, one will need to make sure that Elastic Beanstalk instances can pull the image from the repo. For more info on this check out [this link](https://stackoverflow.com/questions/44850578/aws-elastic-beanstalk-with-amazon-ecr-docker-image).
