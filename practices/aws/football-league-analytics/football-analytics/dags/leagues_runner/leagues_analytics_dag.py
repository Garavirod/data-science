"""
*************************************************************
Author = @Garavirod                                         *
Date = '12/09/2023'                                         *
Description = Extracting Data from Multiple Football League *
*************************************************************
"""

from datetime import datetime, timedelta
import os
from airflow.models import Variable
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.snowflake_operator import SnowflakeOperator
import snowflake.connector as sf
import pandas as pd
import os
from leagues_builder_data.builder import data_processing
from datetime import datetime


default_arguments = {
    'owner': 'RodrigoGar',
    'email': '',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

DAG_NAME = 'FOOTBALL_LEAGUES'
with DAG(DAG_NAME,
         default_args=default_arguments,
         description='Extracting Data Footbal League',
         start_date=datetime(2022, 9, 21),
         schedule_interval=None,
         tags=['tabla_espn'],
         catchup=False) as dag:

    # Getting environment variables
    environment_variable_name = 'feature_info'
    params_info = Variable.get(environment_variable_name, deserialize_json=True)

    # Building data frames
    df = pd.read_csv(
        '/usr/local/airflow/dags/leagues_runner/resources/df_ligas.csv')
    
    df_team = pd.read_csv(
        '/usr/local/airflow/dags/leagues_runner/resources/team_table.csv')

    def extract_info(df, df_team, **kwargs):

        df_data = data_processing(df)
        df_final = pd.merge(df_data, df_team, how='inner', on='team')
        df_final = df_final[['id', 'team', 'played', 'won', 'tied', 'lost', 'goals_favor', 'goals_against', 'diff', 'scores', 'league',
                             'created_at']]

        df_final.to_csv('./premier_positions.csv', index=False)

    # Task definition
    extract_data = PythonOperator(
        task_id='extract_football_data',
        provide_context=True,
        python_callable=extract_info,
        op_kwargs={"df": df, "df_team": df_team}
    )

    upload_stage = SnowflakeOperator(

        task_id='upload_data_stage',
        sql='./queries/upload_stage.sql',
        snowflake_conn_id='snowflake_connection',
        warehouse=params_info["DWH"],
        database=params_info["DB"],
        role=params_info["ROLE"],
        params=params_info
    )
    ingest_table = SnowflakeOperator(

        task_id='ingest_table',
        sql='./queries/upload_table.sql',
        snowflake_conn_id='snowflake_connection',
        warehouse=params_info["DWH"],
        database=params_info["DB"],
        role=params_info["ROLE"],
        params=params_info
    )

    extract_data >> upload_stage >> ingest_table
