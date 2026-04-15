from __future__ import annotations

import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, trim, upper

# This is a file which includes logic for data ingestion

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--env", required=True)
    return parser.parse_args()


def main():
    args = parse_args()

    spark = SparkSession.builder.appName("PIPE-2 Create source to bronze").getOrCreate()

    catalog = args.catalog
    schema = args.schema

    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")

    source_data = [
        (1, "Alice   ", "india", 100.0),
        (2, " Bob", "usa", 250.0),
        (3, "Charlie", "uk", 300.0),
        (4, "   ", "india", 50.0),
        (5, "Eve", "mars", -5.0),
    ]

    df = spark.createDataFrame(
        source_data,
        ["customer_id", "customer_name", "country", "amount"],
    )

    bronze_df = (
        df.withColumn("customer_name", trim(col("customer_name")))
        .withColumn("country", upper(trim(col("country"))))
        .withColumn("ingestion_status", lit("BRONZE_LOADED"))
        .withColumn("env", lit(args.env))
    )

    target_table = f"{catalog}.{schema}.bronze_customers"

    bronze_df.write.mode("overwrite").saveAsTable(target_table)

    print(f"PIPE-2 completed successfully. Data written to {target_table}")


if __name__ == "__main__":
    main()