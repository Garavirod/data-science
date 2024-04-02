from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import json
import requests
from kafka import KafkaProducer
import time
import logging

default_args = {
    'owner': 'airscholar',
    'start_date': datetime(2023, 8, 3, 10, 00)
}


def get_data():
    res = requests.get('https://randomuser.me/api/')
    res = res.json()
    res = res['results'][0]
    return res


def format_data(res: dict):
    data = {}
    location = res['location']
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{location['street']['number']} {location['street']['name']} {location['city']} {location['state']} {location['country']}"
    data['postcode'] = location['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']
    return data


def stream_data():
    producer = KafkaProducer(
        bootstrap_servers=['broker:29092'], max_block_ms=5000)
    topic = 'users_created'
    curr_time = time.time()
    while True:
        if time.time() > curr_time + 60:  # 1
            break
        try:
            data = get_data()
            data = format_data(res=data)
            producer.send(topic=topic, value=json.dumps(data).encode('utf-8'))
        except Exception as e:
            logging.error(f'An error ocurred >: {e}')
            continue


# DAG definitions
with DAG('user_automation',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    streaming_tasks = PythonOperator(
        task_id='stream_data_from_api',
        python_callable=stream_data
    )
