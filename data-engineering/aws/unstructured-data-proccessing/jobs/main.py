from pyspark.sql import SparkSession
from config.config import configuration
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType, DoubleType, DateType
from udf_utils import *
from pyspark.sql.functions import udf, regexp_replace
from pyspark.sql.dataframe import DataFrame


def define_udfs():
    return {
        'extract_file_name_udf': udf(extract_file_name, StringType()),
        'extract_position_udf': udf(extract_position, StringType()),
        'extract_salary_udf': udf(extract_salary, StructType([
            StructField('salary_start', DoubleType(), True),
            StructField('salary_end', DoubleType(), True),
        ])),
        'extract_date_udf': udf(extract_start_date, DateType()),
        'extract_end_date_udf': udf(extract_end_date, DateType()),
        'extract_class_code_udf': udf(extract_class_code, StringType()),
        'extract_requirements_udf': udf(extract_requirements, StringType()),
        'extract_notes_udf': udf(extract_notes, StringType()),
        'extract_duties_udf': udf(extract_duties, StringType()),
        'extract_selection_udf': udf(extract_selection, StringType()),
        'extract_experience_length_udf': udf(extract_experience_length, StringType()),
        'extract_education_length_udf': udf(extract_eduction_length, StringType()),
        'extract_application_location_udf': udf(extract_application_location, StringType()),

    }


if __name__ == '__main__':
    spark = (SparkSession.builder.appName('AWS_Spark_Unstructured')
             .config(
             'spark.jars.packages',
             "org.apache.hadoop:hadoop-aws:3.3.1,"
             "com.amazonaws:aws-java-sdk:1.11.469")
             .config('spark.hadoop.fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')
             .config('spark.hadoop.fs.s3a.access.key', configuration.get('AWS_ACCESS_KEY'))
             .config('spark.hadoop.fs.s3a.secret.key', configuration.get('AWS_SECRET_KEY'))
             .config('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')
             .getOrCreate())

    # For local debugging
    # text_input_dir = 'file:////mnt/c/Users/user/Documents/data-science/data-engineering/aws/unstructured-data-proccessing/input/input_text'
    # csv_input_dir = 'file:////mnt/c/Users/user/Documents/data-science/data-engineering/aws/unstructured-data-proccessing/input/input_csv'
    # json_input_dir = 'file:////mnt/c/Users/user/Documents/data-science/data-engineering/aws/unstructured-data-proccessing/input/input_json'
    # pdf_input_dir = 'file:////mnt/c/Users/user/Documents/data-science/data-engineering/aws/unstructured-data-proccessing/input/input/input_pdf'
    # video_input_dir = 'file:////mnt/c/Users/user/Documents/data-science/data-engineering/aws/unstructured-data-proccessing/input/input_video'
    # img_input_dir = 'file:////mnt/c/Users/user/Documents/data-science/data-engineering/aws/unstructured-data-proccessing/input/input_img'

    # For cluster workers debugging
    text_input_dir = 'file:///opt/bitnami/spark/jobs/input/input_text'
    csv_input_dir = 'file:///opt/bitnami/spark/jobs/input/input_csv'
    json_input_dir = 'file:///opt/bitnami/spark/jobs/input/input_json'
    pdf_input_dir = 'file:///opt/bitnami/spark/jobs/input/input_pdf'
    video_input_dir = 'file:///opt/bitnami/spark/jobs/input/input_video'
    img_input_dir = 'file:///opt/bitnami/spark/jobs/input/input_img'

    # Data schema definition

    data_schema = StructType([
        StructField('file_name', StringType(), True),
        StructField('position', StringType(), True),
        StructField('class_code', StringType(), True),
        StructField('salary_start', DoubleType(), True),
        StructField('salary_end', DoubleType(), True),
        StructField('start_date', DateType(), True),
        StructField('end_date', DateType(), True),
        StructField('req', StringType(), True),
        StructField('notes', StringType(), True),
        StructField('duties', StringType(), True),
        StructField('selection', StringType(), True),
        StructField('experience_length', StringType(), True),
        StructField('job_type', StringType(), True),
        StructField('education_length', StringType(), True),
        StructField('school_type', StringType(), True),
        StructField('application_location', StringType(), True),
    ])

    defined_functions = define_udfs()

    job_bulletin_df = (
        spark.readStream
        .format('text')
        .option('wholetext', 'true')
        .load(text_input_dir)
    )

    json_df = spark.readStream.json(
        json_input_dir, schema=data_schema, multiLine=True)

    job_bulletin_df = job_bulletin_df.withColumn(
        'file_name',
        regexp_replace(
            defined_functions['extract_file_name_udf']('value'),
            r'\r',
            ' '
        )
    )

    job_bulletin_df = job_bulletin_df.withColumn(
        'value',
        regexp_replace(
            'value',
            r'\n',
            ' '
        )
    )

    job_bulletin_df = job_bulletin_df.withColumn(
        'position',
        regexp_replace(
            defined_functions['extract_position_udf']('value'),
            r'\r',
            ' '
        )
    )

    job_bulletin_df = job_bulletin_df.withColumn(
        'salary_start',
        defined_functions['extract_salary_udf'](
            'value').getField('salary_start')
    )

    job_bulletin_df = job_bulletin_df.withColumn(
        'salary_end',
        defined_functions['extract_salary_udf']('value').getField('salary_end')
    )

    job_bulletin_df = job_bulletin_df.withColumn(
        'start_date',
        defined_functions['extract_date_udf']('value')
    )

    job_bulletin_df = job_bulletin_df.withColumn(
        'end_date',
        defined_functions['extract_end_date_udf']('value')
    )
    job_bulletin_df = job_bulletin_df.withColumn(
        'class_code',
        defined_functions['extract_class_code_udf']('value')
    )
    job_bulletin_df = job_bulletin_df.withColumn(
        'requirements',
        defined_functions['extract_requirements_udf']('value')
    )
    job_bulletin_df = job_bulletin_df.withColumn(
        'notes',
        defined_functions['extract_notes_udf']('value')
    )
    job_bulletin_df = job_bulletin_df.withColumn(
        'duties',
        defined_functions['extract_duties_udf']('value')
    )
    job_bulletin_df = job_bulletin_df.withColumn(
        'selection',
        defined_functions['extract_selection_udf']('value')
    )
    job_bulletin_df = job_bulletin_df.withColumn(
        'experience_length',
        defined_functions['extract_experience_length_udf']('value')
    )
    job_bulletin_df = job_bulletin_df.withColumn(
        'eduction_length',
        defined_functions['extract_education_length_udf']('value')
    )
    job_bulletin_df = job_bulletin_df.withColumn(
        'application_location',
        defined_functions['extract_application_location_udf']('value')
    )

    job_bulletin_df = job_bulletin_df\
        .select('file_name',
                'start_date',
                'end_date',
                'salary_start',
                'salary_end',
                'class_code',
                'requirements',
                'notes',
                'duties',
                'selection',
                'experience_length',
                'eduction_length',
                'application_location')

    json_df = json_df\
        .select('file_name',
                'start_date',
                'end_date',
                'salary_start',
                'salary_end',
                'class_code',
                'req',
                'notes',
                'duties',
                'selection',
                'experience_length',
                'education_length',
                'application_location')

    union_data_frame = job_bulletin_df.union(json_df)

    def stream_writer(input: DataFrame, checkpoint_folder, output):
        return (
            input.writeStream
            .format('parquet')
            .option(key='checkpointLocation', value=checkpoint_folder)
            .option(key='path', value=output)
            .outputMode('append')
            .trigger(processingTime='5 seconds')
            .start()
        )

    # query = (
    #     union_data_frame
    #     .writeStream
    #     .outputMode('append')
    #     .format('console')
    #     .option('truncate', False)
    #     .start()
    # )

    query = stream_writer(
        input=union_data_frame, 
        checkpoint_folder=configuration.get('INPUT_FILE'), 
        output='OUTPUT_FILES')

    query.awaitTermination()
