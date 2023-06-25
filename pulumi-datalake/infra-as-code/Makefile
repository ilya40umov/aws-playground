SHELL := bash
aws_profile ?= ilya40umov

purge-glue:
	aws --profile $(aws_profile) glue delete-database --name csv2parquet

purge-s3:
	aws --profile $(aws_profile) s3 rm --recursive s3://$(shell pulumi stack output raw_zone_bucket)/ --exclude="*" --include="/manual_uploads/*"
	aws --profile $(aws_profile) s3 rm --recursive s3://$(shell pulumi stack output raw_zone_bucket)/ --exclude="*" --include="/manual_uploads_v2/*"
	aws --profile $(aws_profile) s3 rm --recursive s3://$(shell pulumi stack output clean_zone_bucket)/ --exclude="*" --include="/csv2parquet/*"
