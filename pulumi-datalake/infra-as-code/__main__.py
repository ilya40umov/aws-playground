import pulumi
from modules.s3_buckets import S3Buckets
from modules.sns_topics import SnsTopics
from modules.csv2parquet_lambda import Csv2ParquetLambda
from modules.csv2parquet_step_fun import Csv2ParquetStepFunction
from modules.csv2parquet_glue import Csv2ParquetGlue
from modules.s3_subscriptions import S3Subscriptions

if __name__ == "__main__":
    provider_config = pulumi.Config("aws")
    aws_region = provider_config.require("region")

    # create raw/clean/curated zones
    s3_buckets = S3Buckets()

    # create SNS topic for reporting errors
    sns_topics = SnsTopics()

    # create lambda that converts CSV files to Parquet files and moves them to clean zone
    csv2parquet_lambda = Csv2ParquetLambda(s3_buckets)

    # create step function that executes previously created lambda, but checks file extension first
    csv2parquet_step_fun = Csv2ParquetStepFunction(
        aws_region, csv2parquet_lambda, sns_topics
    )

    # this will:
    # 1. subscribe csv2parquet lambda to S3 uploads into 'manual_uploads/' directory of raw zone
    # 2. subscribe csv2parquet step function to S3 uploads for 'manual_uploads_v2/' directory of raw zone
    s3_subscriptions = S3Subscriptions(
        s3_buckets, csv2parquet_lambda, csv2parquet_step_fun
    )

    # create Glue Workflow that will only work on a specific location with a CSV file
    csv2parquet_glue = Csv2ParquetGlue(s3_buckets)
