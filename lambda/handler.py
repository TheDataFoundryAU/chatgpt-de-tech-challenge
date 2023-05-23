import os
import requests
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
from datetime import datetime

# Get the bucket name, url, latitude, and longitude from environment variables
BUCKET_NAME = os.getenv('BUCKET_NAME')
WEATHER_API_URL = os.getenv('WEATHER_API_URL')
LATITUDE = os.getenv('LATITUDE')
LONGITUDE = os.getenv('LONGITUDE')


def get_weather_data():
    # Get the url from environment variable and add query parameters
    response = requests.get(f'{WEATHER_API_URL}?latitude={LATITUDE}&longitude={LONGITUDE}&hourly=temperature_2m')
    return response.json()

def parse_weather_data(data):
    hourly_data = data.get('hourly', {})
    df = pd.DataFrame(hourly_data)
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)
    return df

def lambda_handler(event, context):
    try:
        data = get_weather_data()
        df = parse_weather_data(data)
    except Exception as e:
        return {'statusCode': 500, 'body': f'Error fetching and parsing weather data: {str(e)}'}

    # Current time (used for partitioning)
    current_time = datetime.now()

    # Define path (folder structure)
    path = f'year={current_time.year}/month={current_time.month}/day={current_time.day}/hour={current_time.hour}/'

    # Convert DataFrame to parquet and save to S3
    try:
        # Create a parquet table from DataFrame and write to S3
        table = pa.Table.from_pandas(df)
        pq.write_to_dataset(table, f's3://{BUCKET_NAME}/{path}', compression='snappy')
    except Exception as e:
        return {'statusCode': 500, 'body': f'Error saving data to S3: {str(e)}'}

    return {'statusCode': 200, 'body': 'Successfully fetched and stored weather data.'}
