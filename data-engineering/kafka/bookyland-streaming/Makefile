local-spark-job-consumer: 
	spark-submit --packages "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org.scala-lang:scala-library:2.12.14" spark-job.py

docker-spin-up: 
	docker compose up --build -d