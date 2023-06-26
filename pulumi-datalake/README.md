# DataLake with Pulumi

## Progress

- [x] **S3** buckets for `raw`, `clean` and `curated` zones are created
- [x] **Lambda** is used to convert files from CSV to Parquet and register them in **Glue Catalog**
- [x] **Athena** can be used to query the ingested data
- [x] **Step Function** is utilized to orchestrate CSV to Parquet conversion
- [x] **Glue workflow** is used to perform CSV to Parquet conversion and some data manipulations
- [ ] **Redshift Spectrum** is used to load data into the data warehouse
- [ ] **DMS** is setup to provide a CDC for a PostgreSQL database running on **RDS**

## Links

### Sample Datasource

* https://datahub.io/core/population-city

### Docs

* [awswrangler](https://aws-sdk-pandas.readthedocs.io/en/stable/)

