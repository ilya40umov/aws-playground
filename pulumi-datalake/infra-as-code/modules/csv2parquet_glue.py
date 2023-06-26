import json
import pulumi
from pulumi_aws import glue, iam, s3
from modules.s3_buckets import S3Buckets


class Csv2ParquetGlue(object):
    def __init__(self, s3_buckets: S3Buckets):
        self.workflow = glue.Workflow("Csv2ParquetWorkflow")
        self.glue_role = iam.Role(
            "Csv2ParquetWorkflowRole",
            iam.RoleArgs(
                assume_role_policy=json.dumps(
                    {
                        "Version": "2012-10-17",
                        "Statement": [
                            {
                                "Action": "sts:AssumeRole",
                                "Effect": "Allow",
                                "Principal": {
                                    "Service": "glue.amazonaws.com",
                                },
                            },
                        ],
                    }
                ),
                managed_policy_arns=[
                    iam.ManagedPolicy.AMAZON_S3_FULL_ACCESS,  # XXX this is not secure!
                    "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole",
                ],
            ),
        )
        self.job_script = s3.BucketObject(
            "csv2parquet-job.py",
            args=s3.BucketObjectArgs(
                bucket=s3_buckets.glue_jobs_bucket.id,
                source=pulumi.asset.FileAsset("../csv2parquet-glue/csv2parquet-job.py"),
            ),
        )
        self.job = glue.Job(
            "Csv2ParquetJob",
            glue.JobArgs(
                role_arn=self.glue_role.arn,
                glue_version="3.0",
                number_of_workers=2,
                worker_type="G.1X",
                default_arguments={
                    "--RawZoneS3Path": s3_buckets.raw_zone_bucket.bucket.apply(
                        lambda bucket: f"s3://{bucket}/city-population/"
                    ),
                    "--CleanZoneS3Path": s3_buckets.clean_zone_bucket.bucket.apply(
                        lambda bucket: f"s3://{bucket}/cleaned-by-glue/city-population/"
                    ),
                },
                command=glue.JobCommandArgs(
                    script_location=s3_buckets.glue_jobs_bucket.bucket.apply(
                        lambda bucket: f"s3://{bucket}/csv2parquet-job.py"
                    ),
                    python_version="3",
                ),
            ),
        )
        self.catalog_database = glue.CatalogDatabase(
            "CleanedByGlueEtlDatabase",
            glue.CatalogDatabaseArgs(
                name="cleaned-by-glue",
            ),
        )
        self.crawler = glue.Crawler(
            "CleanedByGlueCrawler",
            glue.CrawlerArgs(
                database_name=self.catalog_database.name,
                role=self.glue_role.arn,
                configuration=json.dumps(
                    {
                        "Grouping": {"TableLevelConfiguration": 3},
                        "Version": 1,
                    }
                ),
                s3_targets=[
                    glue.CrawlerS3TargetArgs(
                        path=s3_buckets.clean_zone_bucket.bucket.apply(
                            lambda bucket: f"s3://{bucket}/cleaned-by-glue/"
                        )
                    ),
                ],
            ),
        )
        self.job_trigger = glue.Trigger(
            "Csv2ParquetTrigger",
            type="ON_DEMAND",
            workflow_name=self.workflow.name,
            actions=[
                glue.TriggerActionArgs(
                    job_name=self.job.name,
                )
            ],
        )
        self.crawler_trigger = glue.Trigger(
            "CleanedByGlueCrawlerTrigger",
            type="CONDITIONAL",
            workflow_name=self.workflow.name,
            predicate=glue.TriggerPredicateArgs(
                conditions=[
                    glue.TriggerPredicateConditionArgs(
                        job_name=self.job.name,
                        state="SUCCEEDED",
                    )
                ],
            ),
            actions=[glue.TriggerActionArgs(crawler_name=self.crawler.name)],
        )
