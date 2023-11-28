import json
import boto3
from datetime import datetime
import os
import numpy as np
import requests
import pandas as pd          
import random
import time

s3_client = boto3.client('s3')

def handler(event, context):
    bucket_channel_data_source = os.environ['BUCKET_INPUT_DATA']
    file_name_dataset = os.environ['FILE_CHANNELS_DATA_SET']
    api_key_youtube = os.environ['YOUTUBE_API_KEY']
    bucket_destination = os.environ['BUCKET_OUTPUT_DATA']
    
    # Recover dataset from s3
    obj = s3_client.get_object(
        Bucket=bucket_channel_data_source,
        Key=file_name_dataset
    )

    df_channels = pd.read_csv(obj['Body'])

    # Get statistics
    result = get_channels_statistics(df=df_channels, api_key=api_key_youtube)

    # Save into ephemeral temp
    date = pd.to_datetime('today').strftime('%Y%m%d')
    file_name = f'youtube_stats_{date}.csv'
    file_path = f'/tmp/{file_name}'
    result.to_csv(file_path, index=False)

    # Save file into s3 destination
    s3 = boto3.resource('s3')
    s3.Bucket(bucket_destination).upload_file(file_path, key=file_name)

    # Clear ephemeral temp
    os.remove(file_path)

    return f'{file_path} - Process succeed!'


def make_api_request(channel_id:str, api_key:str)-> dict[str:any]:
    url = f'https://youtube.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}'
    request_response = requests.get(url).json()

    channel_sts = request_response['items'][0]['statistics']

    date = pd.to_datetime('today').strftime('%Y-%m-%d')
    data_channel = {
        'created_at':date,
        'total_views':int(float(channel_sts['viewCount'])),
        'subscribers':int(float(channel_sts['subscriberCount'])),
        'video_count':int(float(channel_sts['videoCount'])),
    }
    return data_channel

def get_channels_statistics(df:pd.DataFrame, api_key:str)->pd.DataFrame:
    """
        Gets the statistics data for every youtube channel in the
        DataFrame
    """
    date = []
    views = []
    subscriber = []
    video_count = []
    channel_name = []
    time_to_sleep_choices = [1,2,3,4,5]

    for i in range(len(df)):
        channel_sts = make_api_request(
            api_key=api_key, 
            channel_id=df['channel_id'][i]
        )

        date.append(channel_sts['created_at'])
        views.append(channel_sts['total_views'])
        subscriber.append(channel_sts['subscribers'])
        video_count.append(channel_sts['video_count'])
        channel_name.append(df['channel_name'][i])

        time.sleep(random.choice(time_to_sleep_choices))
    
    data_result = {
        'Channel_name':channel_name,
        'Subscribers':subscriber,
        'Video_Count':video_count,
        'Total_Views':views,
        'created_at':date,
    }

    df = pd.DataFrame(data_result)
    
    return df