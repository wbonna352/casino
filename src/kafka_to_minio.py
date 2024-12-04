from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F

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
        .withColumn("key", F.col("key").cast("STRING"))
        .withColumn("value", F.col("value").cast("STRING"))
)


def write_df_to_minio(df: DataFrame, table_name: str) -> None:
    (
        df.writeStream
        .format("iceberg")
        .option("checkpointLocation", f"s3a://casino/checkpoint/{table_name}")
        .toTable(table_name)
        .awaitTermination()
    )


if __name__ == '__main__':
    df = get_kafka_df("players")
    write_df_to_minio(df, "players")
