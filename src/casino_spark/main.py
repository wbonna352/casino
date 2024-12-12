from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import pyspark.sql.types as T

TIME_ZONE = "Europe/Warsaw"


def default_spark() -> SparkSession:
    return SparkSession.builder \
        .appName("MySparkApp") \
        .master("local[*]") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkCatalog") \
        .config("spark.sql.catalog.spark_catalog.type", "hadoop") \
        .config("spark.sql.catalog.spark_catalog.warehouse", "s3a://casino/warehouse") \
        .config("spark.sql.streaming.checkpointLocation", "s3a://casino/checkpoint/") \
        .config("spark.sql.catalog.spark_catalog.uri", "http://localhost:9000") \
        .config("spark.hadoop.fs.s3a.access.key", "minio") \
        .config("spark.hadoop.fs.s3a.secret.key", "minio123") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9000") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
        .config("spark.jars.packages",
                "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,"
                "org.apache.hadoop:hadoop-aws:3.3.4,"
                "org.apache.hadoop:hadoop-client-api:3.3.4,"
                "org.apache.hadoop:hadoop-client-runtime:3.3.4,"
                "com.amazonaws:aws-java-sdk-bundle:1.12.262,"
                "org.apache.iceberg:iceberg-spark-runtime-3.5_2.13:1.4.0") \
        .getOrCreate()

