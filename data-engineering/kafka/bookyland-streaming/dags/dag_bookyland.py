from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from datalake.generate_dake_data_lake import generate_fake_data_lake
from callables import call_api_for_candidates, call_api_for_getting_discount

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


generate_fake_data_lake = PythonOperator(
    task_id='generate_fake_data_lake',
    python_callable=generate_fake_data_lake,
    dag=dag
)

extract_purchases = PythonOperator(
    task_id='extract_purchases_from_data_lake',
    python_callable=call_api_for_getting_discount
)

save_candidates_response = PythonOperator(
    task_id='save_candidates_response',
    python_callable=call_api_for_candidates,
    dag=dag
)

save_api_criteria_response = PythonOperator(
    task_id='save_api_criteria_response',
    python_callable=call_api_for_getting_discount,
    dag=dag
)