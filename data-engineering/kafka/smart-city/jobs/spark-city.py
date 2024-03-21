from pyspark.sql import SparkSession
from config import configuration
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType, DoubleType


def main():
    spark = SparkSession.builder.appName('SmartCityStreaming')\
        .config("spark.jars.packages",
                "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0,",
                "org.apache.hadoop:hadoop-aws:3.3.1,"
                "com.amazonaws:aws-java-sdk:1.11.469,")\
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")\
        .config("spark.hadoop.fs.s3a.access.key", configuration.get('AWS_ACCESS_KEY'))\
        .config("spark.hadoop.fs.s3a.secret.key", configuration.get('AWS_SECRET_KEY'))\
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.impl.SimpleAWSCredentialsProvider")\
        .getOrCreate()

    # Adjust log level to minimize the console logs
    spark.sparkContext.setLogLevel('WARN')

    # schemas
    vehicle_schema = StructType([
        StructField(name='id', dataType=StringType(), nullable=True),
        StructField(name='device_id', dataType=StringType(), nullable=True),
        StructField(name='timestamp', dataType=TimestampType(), nullable=True),
        StructField(name='location', dataType=StringType(), nullable=True),
        StructField(name='speed', dataType=DoubleType(), nullable=True),
        StructField(name='direction', dataType=StringType(), nullable=True),
        StructField(name='model', dataType=StringType(), nullable=True),
        StructField(name='make', dataType=StringType(), nullable=True),
        StructField(name='year', dataType=IntegerType(), nullable=True),
        StructField(name='fuelType', dataType=StringType(), nullable=True),
    ])


if __name__ == '__main__':
    main()
