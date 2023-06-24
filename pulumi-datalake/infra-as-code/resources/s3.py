from pulumi_aws import s3


class S3Buckets(object):
    def __init__(self):
        self.raw_zone_bucket = s3.Bucket("raw-zone")
        self.clean_zone_bucket = s3.Bucket("clean-zone")
        self.curated_zone_bucket = s3.Bucket("curated-zone")
