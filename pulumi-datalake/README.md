# DataLake with Pulumi

## Test datasources

* https://datahub.io/core/population-city

## S3 buckets

* An **S3** bucket for `landing` / `raw zone`
* An **S3** bucket for `clean zone`
* Aa **S3** bucket for `curated zone`

## Using Lambda for converting file type

* A **Lambda** function is used to convert the file format from CSV to Parquet
* **Glue Catalog** is updated to catalog in the newly added data

## Using Athena to query data

* **Athena** and **Glue Catalog** are used to query the ingested data

## Loading data into Redshift

* **Redshift Spectrum** is used to load data into the data warehouse

## Using Glue workflow & serverless Spark

* **Glue workflow** is setup to to process (e.g. join) data and copy to the curated zone

## Using StepFunctions to orchestrate a workflow

* **Step Function** is utilized to orchestrate a multi-step workflow

### A CDC pipeline with RDS and DMS

* **DMS** is setup to provide a CDC for a PostgreSQL database running on **RDS**
