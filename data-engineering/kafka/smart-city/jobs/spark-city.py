from pyspark.sql import SparkSession
from config import configuration
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType, DoubleType
from pyspark.sql.functions import from_json, col
from pyspark.sql.dataframe import DataFrame


def main():
    spark = SparkSession.builder.appName('SmartCityStreaming')\
        .config("spark.jars.packages",
                "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0,"
                "org.apache.hadoop:hadoop-aws:3.3.1,"
                "com.amazonaws:aws-java-sdk:1.11.469")\
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")\
        .config("spark.hadoop.fs.s3a.access.key", configuration.get('AWS_ACCESS_KEYS'))\
        .config("spark.hadoop.fs.s3a.secret.key", configuration.get('AWS_SECRET_KEYS'))\
        .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider")\
        .getOrCreate()

    # Adjust log level to minimize the console logs
    spark.sparkContext.setLogLevel('WARN')

    # schemas
    vehicle_schema = StructType([
        StructField(name='id', dataType=StringType(), nullable=True),
        StructField(name='deviceId', dataType=StringType(), nullable=True),
        StructField(name='timestamp', dataType=TimestampType(), nullable=True),
        StructField(name='location', dataType=StringType(), nullable=True),
        StructField(name='speed', dataType=DoubleType(), nullable=True),
        StructField(name='direction', dataType=StringType(), nullable=True),
        StructField(name='model', dataType=StringType(), nullable=True),
        StructField(name='make', dataType=StringType(), nullable=True),
        StructField(name='year', dataType=IntegerType(), nullable=True),
        StructField(name='fuelType', dataType=StringType(), nullable=True),
    ])

    gps_schema = StructType([
        StructField(name='id', dataType=StringType(), nullable=True),
        StructField(name='deviceId', dataType=StringType(), nullable=True),
        StructField(name='timestamp', dataType=TimestampType(), nullable=True),
        StructField(name='speed', dataType=DoubleType(), nullable=True),
        StructField(name='direction', dataType=StringType(), nullable=True),
        StructField(name='vehicleType', dataType=StringType(), nullable=True),
    ])

    traffic_camera_schema = StructType([
        StructField(name='id', dataType=StringType(), nullable=True),
        StructField(name='deviceId', dataType=StringType(), nullable=True),
        StructField(name='cameraId', dataType=StringType(), nullable=True),
        StructField(name='timestamp', dataType=TimestampType(), nullable=True),
        StructField(name='location', dataType=StringType(), nullable=True),
        StructField(name='snapshot', dataType=StringType(), nullable=True),
    ])

    weather_schema = StructType([
        StructField(name='id', dataType=StringType(), nullable=True),
        StructField(name='deviceId', dataType=StringType(), nullable=True),
        StructField(name='timestamp', dataType=TimestampType(), nullable=True),
        StructField(name='temperature', dataType=DoubleType(), nullable=True),
        StructField(name='weatherCondition',
                    dataType=StringType(), nullable=True),
        StructField(name='precipitation',
                    dataType=DoubleType(), nullable=True),
        StructField(name='windSpeed', dataType=DoubleType(), nullable=True),
        StructField(name='humidity', dataType=IntegerType(), nullable=True),
        StructField(name='airQualityIndex',
                    dataType=IntegerType(), nullable=True),
    ])

    emergency_schema = StructType([
        StructField(name='id', dataType=StringType(), nullable=True),
        StructField(name='deviceId', dataType=StringType(), nullable=True),
        StructField(name='timestamp', dataType=TimestampType(), nullable=True),
        StructField(name='location', dataType=StringType(), nullable=True),
        StructField(name='incidentId', dataType=StringType(), nullable=True),
        StructField(name='type', dataType=StringType(), nullable=True),
        StructField(name='status', dataType=StringType(), nullable=True),
        StructField(name='description', dataType=StringType(), nullable=True),
    ])

    def read_kafka_topic(topic, schema):
        return (
            spark.readStream
            .format('kafka')
            .option('kafka.bootstrap.servers', 'broker:29092')
            .option('subscribe', topic)
            .option('startingOffsets', 'earliest')
            .load()
            .selectExpr('CAST(value AS STRING)')
            .select(from_json(col('value'), schema).alias('data'))
            .select('data.*')
            .withWatermark(eventTime='timestamp', delayThreshold='5 minutes')
        )

    def stream_writer(input: DataFrame, checkpointFolder, output):
        return (input.writeStream
                .format('parquet')
                .option('checkpointLocation', checkpointFolder)
                .option('path', output)
                .outputMode('append')
                .start()
                )

    # Data frames creation
    vehicle_df = read_kafka_topic(
        'vehicle_data', vehicle_schema).alias('vehicle')
    gps_df = read_kafka_topic(
        'gps_data', gps_schema).alias('gps')
    traffic_df = read_kafka_topic(
        'traffic_data', traffic_camera_schema).alias('traffic')
    weather_df = read_kafka_topic(
        'weather_data', weather_schema).alias('weather')
    emergency_df = read_kafka_topic(
        'emergency_data', emergency_schema).alias('emergency')

    # Joining Data frames by id and timestamp
    bucket_name = 'dev-spk-streaming'

    query1 = stream_writer(input=vehicle_df,
                  checkpointFolder=f's3a://{bucket_name}/checkpoints/vehicle_data',
                  output=f's3a://{bucket_name}/data/vehicle_data')
    query2 = stream_writer(input=gps_df,
                  checkpointFolder=f's3a://{bucket_name}/checkpoints/gps_data',
                  output=f's3a://{bucket_name}/data/gps_data')
    query3 = stream_writer(input=traffic_df,
                  checkpointFolder=f's3a://{bucket_name}/checkpoints/traffic_data',
                  output=f's3a://{bucket_name}/data/traffic_data')
    query4 = stream_writer(input=weather_df,
                  checkpointFolder=f's3a://{bucket_name}/checkpoints/weather_data',
                  output=f's3a://{bucket_name}/data/weather_data')
    query5 = stream_writer(input=emergency_df,
                  checkpointFolder=f's3a://{bucket_name}/checkpoints/emergency_data',
                  output=f's3a://{bucket_name}/data/emergency_data')
    
    query5.awaitTermination()


if __name__ == '__main__':
    main()
