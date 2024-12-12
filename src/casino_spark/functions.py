from casino_spark.main import TIME_ZONE
import pyspark.sql.functions as F
from pyspark.sql import Column


def bigint_to_timestamp(column: Column, time_zone: str = TIME_ZONE) -> Column:
    return F.to_utc_timestamp(
        F.to_timestamp(column / 1_000_000),
        time_zone
    )
