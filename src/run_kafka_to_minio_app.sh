#!/bin/bash

spark-submit \
  --master spark://casino-spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,\
org.apache.hadoop:hadoop-aws:3.3.4,\
org.apache.hadoop:hadoop-client-api:3.3.4,\
org.apache.hadoop:hadoop-client-runtime:3.3.4,\
com.amazonaws:aws-java-sdk-bundle:1.12.262,\
org.apache.iceberg:iceberg-spark-runtime-3.5_2.13:1.4.0\
  --conf "spark.sql.catalog.spark_catalog=org.apache.iceberg.spark.SparkCatalog" \
  --conf "spark.sql.catalog.spark_catalog.type=hadoop" \
  --conf "spark.sql.catalog.spark_catalog.warehouse=s3a://casino/warehouse" \
  --conf "spark.sql.streaming.checkpointLocation=s3a://casino/checkpoint/" \
  --conf "spark.sql.catalog.my_catalog.uri=http://casino-minio:9000" \
  --conf "spark.hadoop.fs.s3a.access.key=minio" \
  --conf "spark.hadoop.fs.s3a.secret.key=minio123" \
  --conf "spark.hadoop.fs.s3a.endpoint=http://casino-minio:9000" \
  --conf "spark.hadoop.fs.s3a.path.style.access=true" \
  --conf "spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem" \
  --conf "spark.hadoop.fs.s3a.aws.credentials.provider=org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider" \
 kafka_to_minio.py
