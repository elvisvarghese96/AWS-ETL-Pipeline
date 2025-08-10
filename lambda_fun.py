import json
import boto3
import pandas as pd
import io
from datetime import datetime

def transform(data):
    orders_data = []
    for order in data:
        for prod in order['products']:
            orders_data.append({
                "order_id": order['order_id'],
                "order_date": order['order_date'],
                "customer_id": order['customer']['customer_id'],
                "customer_name": order['customer']['name'],
                "customer_email": order['customer']['email'],
                "customer_address": order['customer']['address'],
                "product_id": prod['product_id'],
                "product_category": prod['category'],
                "product_name": prod['name'],
                "product_price": prod['price'],
                "product_category": prod['category'],
                "product_quantity": prod['quantity']
            })
    orders_df = pd.DataFrame(orders_data)
    return orders_df
       

def lambda_handler(event, context):
    # TODO implement
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key=event['Records'][0]['s3']['object']['key']
    s3 = boto3.client('s3')
    response = s3.get_object(Bucket=bucket_name, Key=key)

    data = response['Body'].read().decode('utf-8')
    data = json.loads(data)
    orders_df = transform(data)
    
    parquet_buffer = io.BytesIO()
    orders_df.to_parquet(parquet_buffer, index=False, engine='pyarrow')
    

    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")
    staging = f'orders_data_parquet/orders__{timestamp}.parquet'

    s3.put_object(Bucket=bucket_name, Key=staging, Body=parquet_buffer.getvalue())

    crawler_name = 'etl-pipeline-orders'
    glue = boto3.client('glue')
    response = glue.start_crawler(Name=crawler_name)




