from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from purchase_simulator import run_kafka_simulation_producer

default_dag_args = {
    'owner':'Rod',
    'start_date':'',
    'retries':1,
    'retry_delay':timedelta(seconds=5),
}


dag = DAG(
    dag_id='books_purchasing',
    default_args=default_dag_args,
    catchup=False,
    tags=['streaming','book purchasing','kafka'],
    schedule_interval='@daily'
)


start_purchasing_streaming = PythonOperator(
    task_id='books_purchasing_simulator',
    python_callable=run_kafka_simulation_producer,
    dag=dag
)