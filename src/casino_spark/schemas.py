from pyspark.sql.types import *
from pyspark.sql.types import StructType


def get_value_schema(table_fields: StructType) -> StructType:
    return StructType([
        StructField("schema", StructType([
            StructField("type", StringType(), True),
            StructField("fields", StructType([
                StructField("type", StringType(), True),
                StructField("field", StringType(), True)
            ]))
        ])),
        StructField("payload", StructType([
            StructField("before", table_fields),
            StructField("after", table_fields),
            StructField("source", StructType([
                StructField("version", StringType(), False),
                StructField("connector", StringType(), False)
            ]))
        ]))
    ])


db_schemas: dict[str, StructType] = dict(
    players=StructType([
        StructField("id", IntegerType(), False),
        StructField("first_name", StringType(), False),
        StructField("last_name", StringType(), False),
        StructField("email", StringType(), False),
        StructField("account_balance", DoubleType(), False),
        StructField("created_at", LongType(), False),
        StructField("updated_at", LongType(), False)
    ]),
    games=StructType([
        StructField("id", IntegerType(), False),
        StructField("player_id", IntegerType(), False),
        StructField("type", StringType(), False),
        StructField("stake", DoubleType(), False),
        StructField("result", StringType(), False),
        StructField("payout", DoubleType(), False),
        StructField("created_at", LongType(), False),
        StructField("updated_at", LongType(), False)
    ]),
    transactions=StructType([
        StructField("id", IntegerType(), False),
        StructField("player_id", IntegerType(), False),
        StructField("type", StringType(), False),
        StructField("value", DoubleType(), False),
        StructField("created_at", LongType(), False),
        StructField("updated_at", LongType(), False)
    ])
)

