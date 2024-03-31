from datetime import datetime
# from airflow import DAG
# from airflow.operators.python import PythonOperator
import json
import requests

default_args = {
    'owner': 'airscholar',
    'start_date':datetime(2023, 8, 3, 10,00)
}


def get_data():
    res = requests.get('https://randomuser.me/api/')
    res = res.json()
    res = res['results'][0]
    return res

def format_data(res:dict):
    data = {}
    location = res['location']
    data['first_name'] =  res['name']['first']
    data['last_name'] =  res['name']['last']
    data['gender'] =  res['gender']
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
    data = get_data()
    res = format_data(res=data)
    print(res)

# DAG definitions
""" with DAG('user_automation',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:
    
    streaming_tasks = PythonOperator(
        task_id='stream_data_from_api',
        python_callable=stream_data
    )
 """
stream_data()