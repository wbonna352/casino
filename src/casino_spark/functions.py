from casino_spark.main import TIME_ZONE
import pyspark.sql.functions as F
from pyspark.sql import Column, DataFrame, Window


def bigint_to_timestamp(column: Column, time_zone: str = TIME_ZONE) -> Column:
    return F.to_utc_timestamp(
        F.to_timestamp(column / 1_000_000),
        time_zone
    )

def first_record_by_pk(df: DataFrame, pk_cols: list[Column], order_cols: list[Column]) -> DataFrame:
    window = (
        Window
        .partitionBy(pk_cols)
        .orderBy(order_cols)
    )
    
    return (
        df
        .withColumn("rn", F.row_number().over(window))
        .filter(F.col("rn") == 1)
        .drop("rn")
    )