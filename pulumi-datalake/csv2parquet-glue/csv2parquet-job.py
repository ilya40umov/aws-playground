import sys
import json
from awsglue.utils import getResolvedOptions
from awsglue.transforms import ApplyMapping
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.context import SparkContext

glue_context = GlueContext(SparkContext.getOrCreate())
logger = glue_context.get_logger()

logger.info("Started.")

args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "RawZoneS3Path",
        "CleanZoneS3Path",
    ],
)

logger.info("Arguments: " + json.dumps(args))

job = Job(glue_context)
job.init(args["JOB_NAME"], args)

# https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format-csv-home.html
source_df = glue_context.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={"paths": [args["RawZoneS3Path"]]},
    format="csv",
    format_options={"withHeader": True},
)

source_df.printSchema()

# you can read more about the dynamic frame API here:
# https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-dynamic-frame.html
fields_mapped_df = source_df.apply_mapping(
    [
        ("Country or Area", "string", "country", "string"),
        ("City", "string", "city", "string"),
        ("Year", "int", "year", "int"),
        ("Record Type", "string", "record_type", "string"),
        ("Value", "string", "value", "int"),
    ]
)

filtered_df = fields_mapped_df.filter(
    lambda row: row["value"] is not None and row["value"] > 0
)

df_size = filtered_df.count()

if df_size != 0:
    logger.warn(f"Result dynamic frame has {df_size} rows.")
    glue_context.purge_s3_path(args["CleanZoneS3Path"], {"retentionPeriod": 0})
    glue_context.write_dynamic_frame.from_options(
        frame=filtered_df,
        connection_type="s3",
        connection_options={"path": args["CleanZoneS3Path"]},
        format="parquet",
    )
else:
    logger.warn("Resulting dynamic frame is empty.")

job.commit()

logger.info("Finished.")
