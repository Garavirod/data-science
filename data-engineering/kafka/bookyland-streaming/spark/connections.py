from pyspark.sql import SparkSession
import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType


# Create a SparkSession with Kafka support
def spark_connection(app_name:str):
    packages = [
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2",
        "org.scala-lang:scala-library:2.12.14"
    ]
    spark = None
    try:
        spark = SparkSession.builder \
            .appName(app_name) \
            .config("spark.jars.packages", ''.join(packages,',')) \
            .getOrCreate()
        return spark
    except Exception as e:
        logging.error(
            f"Couldn't create the spark session due to exception {e}")
    return spark


# Read data from Kafka topic
def consume_from_kafka(spark_conn, server, topic):
    df = None
    try:
        df = spark_conn \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", server) \
            .option("subscribe", topic) \
            .option('startingOffsets', 'earliest') \
            .load()
    except Exception as e:
        logging.warning(f"kafka dataframe could not be created because: {e}")
    return df


def create_spark_selection(spark_df, schema):
    sel = spark_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col('value'), schema).alias('data')).select("data.*")
    print(sel)
    return sel