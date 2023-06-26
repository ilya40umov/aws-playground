import pulumi
from pulumi_aws import s3


class S3Buckets(object):
    def __init__(self):
        self.raw_zone_bucket = s3.Bucket(
            "RawZoneBucket",
            s3.BucketArgs(
                bucket_prefix="raw-zone-",
            ),
        )
        self.clean_zone_bucket = s3.Bucket(
            "CleanZoneBucket",
            s3.BucketArgs(
                bucket_prefix="clean-zone-",
            ),
        )
        self.curated_zone_bucket = s3.Bucket(
            "CuratedZoneBucket",
            s3.BucketArgs(
                bucket_prefix="curated-zone-",
            ),
        )
        self.glue_jobs_bucket = s3.Bucket(
            "GlueJobsBucket",
            s3.BucketArgs(
                bucket_prefix="glue-jobs",
                force_destroy=True,
            ),
        )

        pulumi.export("raw_zone_bucket", self.raw_zone_bucket.bucket)
        pulumi.export("clean_zone_bucket", self.clean_zone_bucket.bucket)
        pulumi.export("curated_zone_bucket", self.curated_zone_bucket.bucket)
        pulumi.export("glue_jobs_bucket", self.glue_jobs_bucket.bucket)
