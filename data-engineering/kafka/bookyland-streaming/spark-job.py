from spark.connections import spark_connection, consume_from_kafka, create_spark_selection
from utils.constants import BOOKPURCHASING_KAFKA_TOPIC, BROKER_SERVER_1
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, TimestampType

def create_schema():
    schema = StructType([
        StructField("purchase_id", StringType(), True),
        StructField("user_id", StringType(), True),
        StructField("user_name", StringType(), True),
        StructField("user_lastname", StringType(), True),
        StructField("book_id", StringType(), True),
        StructField("book_title", StringType(), True),
        StructField("book_price", DoubleType(), True),
        StructField("user_country", StringType(), True),
        StructField("book_editorial", StringType(), True),
        StructField("user_city", StringType(), True),
        StructField("user_age", IntegerType(), True),
        StructField("purchase_source", StringType(), True),
        StructField("book_genre", StringType(), True),
        StructField("book_author", StringType(), True),
        StructField("book_isbn", StringType(), True),
        StructField("purchase_date", TimestampType(), True),
        StructField("payment_type", StringType(), True),
        StructField("payment_status", StringType(), True),
        StructField("purchase_revenue", DoubleType(), True),
        StructField("money_currency", StringType(), True),
        StructField("book_page_length", IntegerType(), True),
        StructField("book_language", StringType(), True),
        StructField("book_mode", StringType(), True)
    ])
    return schema


if __name__ == '__main__':

    topic = BOOKPURCHASING_KAFKA_TOPIC
    server = BROKER_SERVER_1

    spark = spark_connection("BookPurchasingKafkaStreaming")

    # Connect to kafka for consuming

    spark_df = consume_from_kafka(spark_conn=spark, server=server, topic=topic)

    schema = create_schema()
    selection_sf = create_spark_selection(spark_df=spark_df, schema=schema)


    # Print the data from Kafka topic
    query = selection_sf \
        .writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    query.awaitTermination()
