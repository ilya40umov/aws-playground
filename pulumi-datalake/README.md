# DataLake with Pulumi

## Test datasources

These datasources can be potentially used to test the code:
* https://datahub.io/core/population-city
* https://www.kaggle.com/datasets/PROPPG-PPG/hourly-weather-surface-brazil-southeast-region

## Progress

- [x] **S3** buckets for `raw`, `clean` and `curated` zones are created
- [x] **Lambda** is used to convert files from CSV to Parquet and register them in **Glue Catalog**
- [x] **Athena** can be used to query the ingested data
- [ ] **Step Function** is utilized to orchestrate CSV to Parquet conversion
- [ ] **Glue workflow** is setup to to process (e.g. join) data and copy to the curated zone
- [ ] **Redshift Spectrum** is used to load data into the data warehouse
- [ ] **DMS** is setup to provide a CDC for a PostgreSQL database running on **RDS**

