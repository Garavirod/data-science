from pyspark.sql import SparkSession
from config.config import configuration
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType, DoubleType, DateType
from udf_utils import *
from pyspark.sql.functions import udf


def define_udfs():
    return {
        'extract_file_name_udf': udf(extract_file_name, StringType()),
        'extract_position_udf': udf(extract_position, StringType()),
        'extract_salary_udf': udf(extract_salary, StructType([
            StructField('salary_start',DoubleType(),True),
            StructField('salary_end',DoubleType(),True),
        ])),
        'extract_date_udf': udf(extract_start_date, DateType()),
        'extract_end_date_udf': udf(extract_end_date, DateType()),
        'extract_class_encode_udf': udf(extract_class_code, StringType()),
        'extract_requirements_udf': udf(extract_requirements, StringType()),
        'extract_notes_udf': udf(extract_notes, StringType()),
        'extract_duties_udf': udf(extract_duties, StringType()),
        'extract_selection_udf': udf(extract_selection, StringType()),
        'extract_experience_length_udf': udf(extract_experience_length, StringType()),
        'extract_education_length_udf': udf(extract_eduction_length, StringType()),
        'extract_application_location_udf': udf(extract_application_location, StringType()),
       
    }

if __name__ == '__main__':
    spark = (SparkSession.builder
             .appName('AWS_Spark_Unstructured')
             .config(
                 'spark.jars.packages',
                 'org.apache.hadoop:hadoop-aws:3.3.1,'
                 'com.amazonaws:aws-java-sdk:1.11.469')
             .config('spark.hadoop.fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')
             .config('spark.hadoop.fs.s3a.access.key', configuration.get('AWS_ACCESS_KEY'))
             .config('spark.hadoop.fs.s3a.secret.key', configuration.get('AWS_SECRET_KEY'))
             .config('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')
             .getOrCreate()
             )

    text_input_dir = 'file://C:/Users/user/Documents/data-science/data-engineering/aws/unstructured-data-proccessing/input/input_text'
    csv_input_dir = 'file://C:/Users/user/Documents/data-science/data-engineering/aws/unstructured-data-proccessing/input/input_csv'
    json_input_dir = 'file://C:/Users/user/Documents/data-science/data-engineering/aws/unstructured-data-proccessing/input/input_json'
    pdf_input_dir = 'file://C:/Users/user/Documents/data-science/data-engineering/aws/unstructured-data-proccessing/input/input_pdf'
    video_input_dir = 'file://C:/Users/user/Documents/data-science/data-engineering/aws/unstructured-data-proccessing/input/input_video'
    img_input_dir = 'file://C:/Users/user/Documents/data-science/data-engineering/aws/unstructured-data-proccessing/input/input_img'

    # Data schema definition

    data_schema = StructType([
        StructField('file_name',StringType(), True),
        StructField('position',StringType(), True),
        StructField('class_code',StringType(), True),
        StructField('salary_start',DoubleType(), True),
        StructField('salary_end',DoubleType(), True),
        StructField('start_date',DateType(), True),
        StructField('end_date',DateType(), True),
        StructField('req',StringType(), True),
        StructField('notes',StringType(), True),
        StructField('duties',StringType(), True),
        StructField('selection',StringType(), True),
        StructField('experience_length',StringType(), True),
        StructField('job_type',StringType(), True),
        StructField('education_length',StringType(), True),
        StructField('school_type',StringType(), True),
        StructField('application_location',StringType(), True),
    ])


    udf = define_udfs()

    job_bulletin_df = (
        spark.readSream
        .format('text')
        .option('wholetext','true')
        .load(text_input_dir)
    )

    query = (
        job_bulletin_df
        .writeStream
        .outputMode('append')
        .format('console')
        .start()
    )

    query.awaitTermination()