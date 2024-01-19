import pandas as pd
import json
import random
import time
import hashlib
import os
import uuid
import boto3

CITIES = [
    'Ciudad de México',
    'Guadalajara',
    'Queretaro',
    'Monterrey',
    'Puebla'
]

SOURCE_PURCHASE = ['ONLINE', 'ORGANIC']

PAYMENT_ONLINE = ['Debit', 'Credit']

PAYMENT_STORE = ['Cash', 'Debit', 'Credit']

MARKETING = [
    'Social media',
    'News',
    'Organic'
]


STATUS_PURCHASED = [
    'COMPLETED',
    'REJECTED',
    'INSUFFICIENT_FUNDS',
    'FAILED_API',
    'FRAUD',
    'COMPLETED',
    'COMPLETED',
    'COMPLETED',
]


STORE_COORDS_BY_CITY = {
    'Ciudad de México':[
    (19.372879, -99.049378),
    (19.428502, -99.162914),
    (19.355778, -99.153214),
    (19.355778, -99.153214)],
    'Guadalajara':[
    (20.690072, -103.301842),
    (20.670411, -103.354498),
    (20.693754, -103.381888),],
    'Queretaro':[
    (20.606305, -100.412364),
    (20.623607, -100.440612),
    (20.655995, -100.399978),],
    'Monterrey':[
    (25.713272, -100.277447),
    (25.732508, -100.234559),
    (25.715347, -100.344189),
    (25.744479, -100.409122),],
    'Puebla':[
    (18.973534, -98.252895),
    (18.971747, -98.215115),
    (19.016400, -98.183632),]
}


# Aws auth via boto3
stream_name = 'kinesis_stream_name'
region='us-east-2'
kinesis_client= boto3.client('kinesis', region_name=region)


def get_payment_method(source:str):
    if source == 'ORGANIC':
        payment = random.choice(PAYMENT_STORE)
        status = 'COMPLETED'
        order_type = 'STORE'
    else:
        payment = random.choice(PAYMENT_ONLINE)
        status = random.choice(STATUS_PURCHASED)
        order_type = 'ONLINE'
    
    return payment, status, order_type
    
    
def get_store_coords(city:str):
    return random.choice(STORE_COORDS_BY_CITY[city])
    


def simulate_purchases(num_purchases:int, df_inventory:pd.DataFrame):
    x = 0
    while x >= 0:
        date = pd.to_datetime('today').strftime('%Y-%m-%d %H:%M:%S')
        product = df_inventory['PRODUCT_NAME '][random.randint(0,len(df_inventory)-1)]
        pricing = df_inventory[df_inventory['PRODUCT_NAME '] == product]['PRICING'].values[0]
        commission = df_inventory[df_inventory['PRODUCT_NAME '] == product]['COMISION'].values[0]
        brand = df_inventory[df_inventory['PRODUCT_NAME '] == product]['BRAND'].values[0]
        category = df_inventory[df_inventory['PRODUCT_NAME '] == product]['CATEGORY'].values[0]
        source_purchase = random.choice(SOURCE_PURCHASE)
        payment,status, order_type = get_payment_method(source_purchase)
        city = random.choice(CITIES)
        latitude, longitude = get_store_coords(city)
        marketing = random.choice(MARKETING)

        purchase = {
            'purchase_id':str(uuid.uuid4()),
            'product_name':product,
            'pricing':str(pricing),
            'commission':str(commission),
            'brand':brand,
            'category':category,
            'marketing':marketing,
            'source_purchase':source_purchase,
            'payment':payment,
            'status':status,
            'order_type':order_type,
            'city':city,
            'created_at':date,
            'latitude':str(latitude),
            'longitude':str(longitude),
        }
        # Send record via kinesis
        record = json.dumps(purchase).encode('utf-8')
        records = kinesis_client.put_record(
            StreamName= stream_name,
            Data=record,
            PartitionKey='purchase_id',
            
        )

        x += 1
        time.sleep(random.choice([1,2]))
        requestId = records['ResponseMetadata']['RequestId']
        httpStatusCode = records['ResponseMetadata']['HTTPStatusCode']
        message = f'Total data ingested: {x}, RequestId: {requestId}, Status: {httpStatusCode}'
        print(message)
    


if __name__ == '__main__':
    inventory_df = pd.read_excel('./resources/ecomerce_datexland.xlsx')
    simulate_purchases(num_purchases=20, df_inventory=inventory_df)