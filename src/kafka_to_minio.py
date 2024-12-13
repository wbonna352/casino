from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F
from pyspark.sql.types import StringType
from py4j.protocol import Py4JJavaError

import os
from time import sleep

from casino_spark.schemas import db_schemas, get_value_schema

minioEndpoint = "http://minio:9000"
minioAccessKey = "minio"
minioSecretKey = "minio123"

spark = (
    SparkSession.builder
    # .master("local[*]")
    .config("spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,"
            "org.apache.hadoop:hadoop-aws:3.3.4,"
            "org.apache.hadoop:hadoop-client-api:3.3.4,"
            "org.apache.hadoop:hadoop-client-runtime:3.3.4,"
            "com.amazonaws:aws-java-sdk-bundle:1.12.262")
    .config("spark.hadoop.fs.s3a.endpoint", minioEndpoint)
    .config("spark.hadoop.fs.s3a.access.key", minioAccessKey)
    .config("spark.hadoop.fs.s3a.secret.key", minioSecretKey)
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .config("spark.hadoop.fs.s3a.path.style.access", "true")
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")
    .getOrCreate()
)


def get_kafka_df(table_name: str) -> DataFrame:
    return (
        spark
        .readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "casino-kafka:9090")
        .option("subscribe", f"casino.public.{table_name}")
        .option("startingOffsets", "earliest")
        .load()

        .drop("key")
        .withColumn("value", F.from_json(
            F.col("value").cast(StringType()),
            get_value_schema(db_schemas.get(table_name))
        ))
        .withColumn("value", F.col("value.payload.after"))
    )


def write_df_to_minio(df: DataFrame, table_name: str) -> None:
    (
        df.writeStream
        .format("iceberg")
        .option("checkpointLocation", f"s3a://casino/checkpoint/{table_name}")
        .toTable(table_name)
        .awaitTermination()
    )


def streaming_process(table_name: str) -> None:
    df = get_kafka_df(table_name)
    write_df_to_minio(df, table_name)


if __name__ == '__main__':
    table_name = os.getenv("TABLE_NAME")

    while True:
        try:
            streaming_process(table_name)
            break
        except:
            print("ERROR")
            sleep(5)
