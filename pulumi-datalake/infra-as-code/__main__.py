import pulumi
from resources.s3 import S3Buckets
from resources.csv2parquet import CsvToParquetLambda

if __name__ == "__main__":
    s3_buckets = S3Buckets()
    csv_to_parquet_lambda = CsvToParquetLambda(s3_buckets)
    s3_buckets.subscribe_lambda_to_raw_bucket(
        lambda_arn=csv_to_parquet_lambda.lambda_function.arn,
        filter_prefix="manual_uploads/",
        filter_suffix=".csv"
    )
