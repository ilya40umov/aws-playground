import pulumi
from modules.s3_buckets import S3Buckets
from modules.csv2parquet_lambda import Csv2ParquetLambda
from modules.csv2parquet_step_fun import Csv2ParquetStepFunction
from modules.s3_subscriptions import S3Subscriptions

if __name__ == "__main__":
    # create raw/clean/curated zones
    s3_buckets = S3Buckets()

    # create lambda that converts CSV files to Parquet files and moves them to clean zone
    csv2parquet_lambda = Csv2ParquetLambda(s3_buckets)

    # create step function that executes previously created lambda, but checks file extension first
    csv2parquet_step_fun = Csv2ParquetStepFunction(csv2parquet_lambda)

    # this will:
    # 1. subscribe csv2parquet lambda to S3 uploads into 'manual_uploads/' directory of raw zone
    # 2. subscribe csv2parquet step function to S3 uploads for 'manual_uploads_v2/' directory of raw zone
    s3_subscriptions = S3Subscriptions(
        s3_buckets, csv2parquet_lambda, csv2parquet_step_fun
    )
