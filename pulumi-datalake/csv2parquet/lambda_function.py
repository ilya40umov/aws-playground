import json
import boto3
import os
import awswrangler as wr
from urllib.parse import unquote_plus

DB_NAME = "csv2parquet"


def lambda_handler(event, context):
    bucket = None
    key = None

    if "Records" in event and event["Records"]:
        print("Invoked with S3 payload")
        record = event["Records"][0]
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])
    elif "detail" in event:
        print("Invoked with EventBridge payload")
        bucket = event["detail"]["bucket"]["name"]
        key = unquote_plus(event["detail"]["object"]["key"])
    else:
        print("Unsupported event: " + json.dumps(event, indent=2))
        return "IGNORED"

    print(f"Bucket: {bucket}")
    print(f"Key: {key}")

    key_parts = key.split("/")
    table_name = key_parts[-1].split(".")[0]
    print(f"Table Name: {table_name}")

    db_name = DB_NAME

    input_path = f"s3://{bucket}/{key}"
    input_df = wr.s3.read_csv([input_path])

    current_databases = wr.catalog.databases()
    wr.catalog.databases()
    if db_name not in current_databases.values:
        print(f"[WARN] Database {db_name} does not exist yet. Creating ...")
        wr.catalog.create_database(db_name)

    output_bucket = os.environ["OUTPUT_BUCKET"]
    output_path = f"s3://{output_bucket}/csv2parquet/{db_name}/{table_name}"

    result = wr.s3.to_parquet(
        df=input_df,
        path=output_path,
        dataset=True,
        database=db_name,
        table=table_name,
        mode="append",
    )

    print(f"Outcome: {result}")
    return result
