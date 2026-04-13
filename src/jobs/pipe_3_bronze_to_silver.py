from __future__ import annotations

import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    lit,
    trim,
    upper,
    when,
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--env", required=True)
    return parser.parse_args()


def main():
    args = parse_args()

    spark = SparkSession.builder.appName("PIPE-3 Create bronze to silver by adding DQ rules").getOrCreate()

    catalog = args.catalog
    schema = args.schema

    bronze_table = f"{catalog}.{schema}.bronze_customers"
    silver_table = f"{catalog}.{schema}.silver_customers"

    bronze_df = spark.table(bronze_table)

    country_col = upper(trim(col("country")))
    name_col = trim(col("customer_name"))

    silver_df = (
        bronze_df.withColumn(
            "dq_reason",
            when(col("customer_id").isNull(), lit("customer_id_is_null"))
            .when(name_col == "", lit("customer_name_is_blank"))
            .when(col("amount").isNull() | (col("amount") < 0), lit("amount_is_invalid"))
            .when(~country_col.isin("INDIA", "USA", "UK", "UAE", "CANADA"), lit("country_not_allowed"))
            .otherwise(lit("VALID")),
        )
        .withColumn(
            "dq_status",
            when(col("dq_reason") == "VALID", lit("PASS")).otherwise(lit("FAIL")),
        )
        .withColumn(
            "record_status",
            when(col("dq_status") == "PASS", lit("SILVER_READY")).otherwise(lit("REJECTED")),
        )
        .withColumn("env", lit(args.env))
    )

    silver_df.write.mode("overwrite").saveAsTable(silver_table)

    print(f"PIPE-3 completed successfully. Data written to {silver_table}")


if __name__ == "__main__":
    main()