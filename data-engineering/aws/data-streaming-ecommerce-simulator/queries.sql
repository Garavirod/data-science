-- Create an external table from glue database
CREATE EXTERNAL TABLE `purchases-kinesis` (
	`purchase_id` string,
	`product_name` string,
	`pricing` double,
	`commission` double,
	`brand` string,
	`category` string,
	`marketing` string,
	`source_purchase` string,
	`payment` string,
	`status` string,
	`order_type` string,
	`city` string,
	`created_at` string,
	`latitude` double,
	`longitude` double
)
PARTITIONED BY (
	`year` string,
	`month` string,
	`day` string,
	`hour` string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe'
STORED AS INPUTFORMAT 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION 's3://demo-kds-rga/purchases-kinesis'


-- What is the city with the most purchases ?
SELECT city , status, COUNT(*) AS num_purchases FROM "demo-kds-rga"."purchases-kinesis" 
where status = 'COMPLETED'
group BY city, status